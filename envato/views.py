import json
import os
import threading

import jdatetime
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.cache import never_cache
from custom_logs.models import custom_log
from envato.models import EnvatoFile, EnvatoUserFile


class RequestFile(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'ثبت نام کاربر جدید'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        front_input = json.loads(request.body)
        try:
            user_telegram_phone_number = front_input['user_telegram_phone_number']
            user_unique_id = front_input['user_unique_id']
            secret_token = front_input['secret_token']
            file_page_link = front_input['file_page_link']
            user = User.objects.get(username=user_unique_id)
            if user.profile.vip_expiry_date > jdatetime.datetime.now(): ## سیستم اشتراکی
                try:
                    envato_file = EnvatoFile.objects.get(link=file_page_link)
                    try:
                        envato_user_file = EnvatoUserFile.objects.get(user=user, file=envato_file)
                        if envato_file.file is not None:
                            return JsonResponse({'message': envato_file.file.url})
                        else:
                            return JsonResponse({'message': 'لینک فایل بزودی برای شما ارسال می شود'})
                    except:
                        envato_user_file = EnvatoUserFile(
                            user=user,
                            file=envato_file,
                            is_single_pay=False,
                        )
                        envato_user_file.save()
                except:
                    new_envato_file = EnvatoFile(
                        link=file_page_link,
                    )
                    new_envato_file.save()
                    new_envato_user_file = EnvatoUserFile(
                        user=user,
                        file=new_envato_file,
                        is_single_pay=False,
                    )
                    new_envato_user_file.save()
                    return JsonResponse({'message': 'لینک فایل بزودی برای شما ارسال می شود'})
            else:
                pass ## سیستم پرداخت تکی
        except Exception as e:
            return JsonResponse({'message': 'input arguments are not correct. err: ' + str(e)})
