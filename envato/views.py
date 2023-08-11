import json
import threading
import time

import jdatetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View

from accounts.models import UserRequestHistory
from envato.enva_def import EnvatoSignInThread
from envato.models import EnvatoFile
from envato.tasks import EnvatoScraperThread
from envato.utils import telegram_http_send_message
from custom_logs.models import custom_log


def envato_auth_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            EnvatoSignInThread().start()
            return JsonResponse({'message': 'envato_auth: sign-in function has been started'})
        else:
            return JsonResponse({'message': 'not allowed'})
    else:
        return JsonResponse({'message': 'not allowed'})


def envato_scraper_start_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            EnvatoScraperThread().start()
            return JsonResponse({'message': 'envato_scraper: scraper has been started'})
        else:
            return JsonResponse({'message': 'not allowed'})
    else:
        return JsonResponse({'message': 'not allowed'})


class RequestFile(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'ثبت نام کاربر جدید'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            secret_key = request.META['HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN']
            custom_log('secret_key: ' + str(secret_key))
        except:
            secret_key = None
            custom_log('secret_key is none')
        if secret_key is not None and str(secret_key) == '12587KFlk54NCJDmvn8541':
            front_input = json.loads(request.body)
            custom_log(str(front_input))
            try:
                user_unique_id = front_input['message']['from']['id']
                user_first_name = front_input['message']['from']['first_name']
                file_page_link = str(front_input['message']['text']).split()
                custom_log(str(user_unique_id))
                custom_log(str(user_first_name))
                custom_log(str(file_page_link))
                try:
                    user = User.objects.get(username=user_unique_id)
                except:
                    user = User.objects.create_user(username=user_unique_id, first_name=user_first_name)

                if user.profile.vip_expiry_date > jdatetime.datetime.now():  ## سیستم اشتراکی
                    today = jdatetime.datetime.today()
                    date_time_from = jdatetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, microsecond=0)
                    date_time_to = jdatetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, microsecond=999)
                    today_user_request_history = UserRequestHistory.objects.filter(user=user, created_at__range=[date_time_from, date_time_to])
                    if today_user_request_history.count() > user.profile.allowed_request_per_day:
                        telegram_http_send_message(user_id=user_unique_id,
                                                   message='تعداد درخواست های مجاز روزانه شما به حداکثر رسیده است')
                        return JsonResponse(
                            {'message': 'RequestFile-> درخواست های مجاز روزانه این کاربر به حداکثر رسیده است'})

                    file_page_link_list = []
                    for i in file_page_link:
                        if i.find('https://elements.envato.com') != -1:
                            if len(file_page_link_list) <= user.profile.allowed_request_per_day:
                                file_page_link_list.append(i)
                    custom_log(str(file_page_link_list))
                    custom_log('RequestFile-> درخواست توسط پردازشگر ربات در حال بررسی می باشد')
                    telegram_http_send_message(user_id=user_unique_id,
                                               message='درخواست توسط پردازشگر ربات در حال بررسی می باشد')
                    time.sleep(1)
                    RequestHandler(user=user, file_page_link_list=file_page_link_list).start()
                    return JsonResponse({'message': 'RequestFile-> درخواست توسط پردازشگر ربات در حال بررسی می باشد'})
                else:
                    custom_log('RequestFile-> کاربر بدون اشتراک فعال است و امکان درخواست فایل ندارد')
                    telegram_http_send_message(user_id=user_unique_id,
                                               message='اشتراک فعالی ندارید. جهت تهیه اشتراک بر روی لینک زیر کلیک نمایید: https://maxish.ir')
                    return JsonResponse({'message': 'RequestFile-> کاربر بدون اشتراک فعال است و امکان درخواست فایل ندارد'})
            except Exception as e:
                custom_log('RequestFile->try/except. err: ' + str(e))
                return JsonResponse({'message': 'RequestFile->try/except. err: ' + str(e)})
        else:
            return JsonResponse({'message': 'not allowed, sk'})


class RequestHandler(threading.Thread):
    def __init__(self, user, file_page_link_list):
        super().__init__()
        self.user = user
        self.file_page_link_list = file_page_link_list

    def run(self):
        if len(self.file_page_link_list) == 0:
            custom_log('RequestFile-> درخواست نامعتبر است. لینک انواتو یافت نشد')
            telegram_http_send_message(self.user.username, 'درخواست نامعتبر است. لینک انواتو یافت نشد')
            return False
        for link in self.file_page_link_list:
            try:
                envato_file = EnvatoFile.objects.get(page_link=link)  # فایل از قبل موجود است
                try:  # مواردی که اطلاع رسانی نشده اند بررسی میشود
                    user_request_history = UserRequestHistory.objects.get(user=self.user, file=envato_file,
                                                                          is_noticed=False)
                    if envato_file.file != '':
                        pass
                    else:
                        # فایل پس از تکمیل دانلود برای یوزر ارسال شود
                        telegram_http_send_message(user_id=self.user.username,
                                                   message='لینک دریافت فایل پس از تکمیل دانلود برای شما ارسال خواهد شد')
                except:
                    user_request_history = UserRequestHistory(
                        user=self.user,
                        file=envato_file,
                        is_single_pay=False,
                    )
                    user_request_history.save()
                    if envato_file.file != '':
                        pass
                    else:
                        telegram_http_send_message(user_id=self.user.username, message='لینک دریافت فایل پس از تکمیل دانلود برای شما ارسال خواهد شد')
            except:  # فایل از قبل موجود نیست
                new_envato_file = EnvatoFile(
                    page_link=link,
                )
                new_envato_file.save()
                new_envato_user_file = UserRequestHistory(
                    user=self.user,
                    file=new_envato_file,
                    is_single_pay=False,
                )
                new_envato_user_file.save()
                # فایل پس از تکمیل دانلود برای یوزر ارسال شود
                telegram_http_send_message(user_id=self.user.username, message='لینک دریافت فایل پس از تکمیل دانلود برای شما ارسال خواهد شد')
        return True



