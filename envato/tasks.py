import random
import threading
import time

from accounts.models import UserRequestHistory
from custom_logs.models import custom_log
from envato.enva_def import envato_download_file, envato_auth
from envato.models import EnvatoFile, get_envato_config_settings, EnvatoActiveThread
from envato.utils import telegram_http_send_message


def envato_scraper():
    custom_log("envato user request handler thread: function has been started", "d")
    EnvatoUserRequestHandlerThread().start()

    custom_log("envato_auth: sign-in function has been started", "d")
    envato_auth()
    custom_log("envato_auth: sign-in function has been finished", "d")
    custom_log("envato_auth: waiting for 5 seconds after envato_auth function", "d")
    time.sleep(5)
    while True:
        while not get_envato_config_settings().login_status:
            custom_log("login_status: waiting for user to start sigh-in function", "d")
            time.sleep(5)
        envato_active_threads_number = EnvatoActiveThread.objects.all().count()
        if envato_active_threads_number < get_envato_config_settings().envato_thread_number:
            envato_files = EnvatoFile.objects.filter(file='', in_progress=False, is_acceptable_file=True)[
                           :get_envato_config_settings().envato_queue_number]
            for file in envato_files:
                file.in_progress = True
                file.save()
            if envato_files.count() > 0:
                EnvatoDownloadFileThread(envato_files=envato_files, name=str(random.randint(1, 9999))).start()
                EnvatoActiveThread.objects.create()
            else:
                custom_log("envato_scraper, there is no file to download. we are waiting for 5 seconds", "d")
        else:
            custom_log("number of active threads: " + str(envato_active_threads_number), "d")
        time.sleep(5)


class EnvatoDownloadFileThread(threading.Thread):
    def __init__(self, envato_files, name=None):
        super().__init__()
        self._name = name
        self.envato_files = envato_files

    def run(self):
        try:
            custom_log("envato_thread: start action", "d")
            for file in self.envato_files:
                file.in_progress = True
                file.save()
            envato_download_file(self.envato_files)
            EnvatoActiveThread.objects.all().latest('id').delete()
            for file in self.envato_files:
                file.in_progress = False
                file.save()
            custom_log("envato_thread: finished", "d")
            return True
        except Exception as e:
            EnvatoActiveThread.objects.all().latest('id').delete()
            for file in self.envato_files:
                file.in_progress = False
                file.save()
            custom_log("try/except->envato_thread. err: " + str(e), "d")


class EnvatoScraperThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            envato_scraper()
        except Exception as e:
            custom_log("EnvatoScraperThread:try/except-> err: " + str(e), "d")


class EnvatoUserRequestHandlerThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            notice_user_if_file_has_been_downloaded()
        except Exception as e:
            custom_log("EnvatoUserRequestHandlerThread:try/except-> err: " + str(e), "d")


def notice_user_if_file_has_been_downloaded():
    while True:
        user_requests_history = UserRequestHistory.objects.filter(is_noticed=False)
        for user_request in user_requests_history:
            if user_request.file.file != '':
                telegram_http_send_message(user_id=user_request.user.username, message='https://envato.maxish.ir' + str(user_request.file.file.url))
                user_request.is_noticed = True
                user_request.save()
                time.sleep(1)

