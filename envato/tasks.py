import random
import threading
import time

from accounts.models import UserRequestHistory
from custom_logs.models import custom_log
from envato.enva_def import envato_download_file, envato_auth
from envato.models import EnvatoFile, get_envato_config_settings, EnvatoActiveThread


def envato_scraper():
    # custom_log("envato_auth: sign-in function has been started", "d")
    # envato_auth()
    # custom_log("envato_auth: sign-in function has been finished", "d")
    # custom_log("envato_auth: waiting for 60 seconds after envato_auth function", "d")
    # time.sleep(60)
    while True:
        while not get_envato_config_settings().login_status:
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


def notice_user_if_file_has_been_downloaded():
    user_requests_history = UserRequestHistory.objects.filter(is_noticed=False, file__file=not '')
    for user_request in user_requests_history:
        # notice function
        pass
