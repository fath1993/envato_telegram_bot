from django.views import View
from django.contrib.auth.models import User
from accounts.models import Profile
from django.http import JsonResponse
import json


class SignUp(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'ثبت نام کاربر جدید'}

    def get(self, request, *args, **kwargs):
        json_response_body = {
            'request': 'ثبت نام کاربر جدید',
            'راهنمایی استفاده از متد های REST': {
                'پیش فرض': {
                    'توضیحات': 'متد بصورت عمومی قابل دسترس می باشد',
                },
                'GET': {
                    'توضیحات': 'راهنمایی های لازم در خصوص استفاده از API مربوطه',
                    'سبک داده مورد پذیرش': 'وارد کردن لینک API بصورت مستقیم از طریق مرورگر',
                },
                'POST': {
                    'توضیحات': 'از طریق این متد امکان ثبت نام کاربر جدید در ربات تلگرام مکسیش فراهم شده است',
                    'سبک داده مورد پذیرش': 'json جیسون',
                    'داده های ارسالی': {
                        'user_telegram_phone_number': 'شماره تلگرام کاربر',
                        'user_unique_id': 'آیدی یکتای کاربر',
                        'secret_token': 'توکن متصل به وبهوک',
                    },
                    'خطا های احتمالی': {
                        'فرمت ورودی صحیح نمی باشد': 'جیسون ارسالی شامل مقادیر از پیش مشخص شده نیست یا بدرستی ارسال نشده است',
                        'شماره همراه ارائه شده در سیستم موجود می باشد': 'شماره همراه ارائه شده در سیستم موجود می باشد',
                        'موفق - نا تمام': 'ثبت نام کاربر نا تمام است. جهت تکمیل ثبت نام و ایجاد حساب کاربری مرحله اکانت وریفای صورت پذیرد',
                    }
                },
            }
        }
        return JsonResponse(json_response_body)

    def post(self, request, *args, **kwargs):
        front_input = json.loads(request.body)
        try:
            user_telegram_phone_number = front_input['user_telegram_phone_number']
            user_unique_id = front_input['user_unique_id']
            secret_token = front_input['secret_token']

            if user_telegram_phone_number is None or user_unique_id is None or secret_token is None:
                return JsonResponse({'message': 'failed'})
            try:
                user = User.objects.get(username=user_unique_id)
                return JsonResponse({'message': 'user has exist'})
            except:
                user = User.objects.create_user(username=user_unique_id)
                profile = Profile.objects.get(user=user)
                profile.user_telegram_phone_number = user_telegram_phone_number
                profile.save()
                return JsonResponse({'message': 'user has been registered'})
        except Exception:
            return JsonResponse({'message': 'inputs are not corrects'})


# class ProfileSingle(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (CustomIsAuthenticated,)
#
#     def get(self, request, *args, **kwargs):
#         json_response_body = {
#             'request': 'جزئیات حساب کاربری',
#             'راهنمایی استفاده از متد های REST': {
#                 'پیش فرض': {
#                     'توضیحات': 'ضمیمه هدر توکن فعال کاربر می باشد',
#                     'نمونه': 'Authorization: Token a4a3b0b69cca4c4ce4ae58023be4b4f601a604ed3be9cc0797ec53d3e01a6551',
#                 },
#                 'GET': {
#                     'توضیحات': 'راهنمایی های لازم در خصوص استفاده از API مربوطه',
#                     'سبک داده مورد پذیرش': 'وارد کردن لینک API بصورت مستقیم از طریق مرورگر',
#                 },
#                 'POST': {
#                     'توضیحات': 'از طریق این متد امکان بررسی جزئیات حساب کاربری فراهم شده است',
#                     'سبک داده مورد پذیرش': 'json جیسون',
#                     'داده های ارسالی': 'ندارد',
#                     'خطا های احتمالی': {
#                         'نامشخص': 'خطای سیستم'
#                     },
#                 },
#                 'PUT': {
#                     'توضیحات': 'از طریق این متد امکان ویرایش حساب کاربری فراهم شده است',
#                     'سبک داده مورد پذیرش': 'json جیسون',
#                     'داده های ارسالی': {
#                         'new_password': 'کلمه عبور جدید',
#                         'email': 'ایمیل',
#                         'biography': 'درباره کاربر',
#                         'profile_pic_id': 'آیدی تصویر پروفایل',
#                     },
#                     'خطا های احتمالی': {
#                         'فرمت ورودی صحیح نمی باشد': 'داده های ارسالی کامل نیست یا بدرستی ارسال نشده است',
#                         'تصویر با ایدی ارائه شده وجود ندارد': 'تصویری با آیدی ارسال شده وجود ندارد',
#                     }
#                 },
#                 'DELETE': {
#                     'توضیحات': 'از طریق این متد امکان حذف حساب کاربری فراهم شده است',
#                     'سبک داده مورد پذیرش': 'json جیسون',
#                     'داده های ارسالی': 'ندارد',
#                     'خطا های احتمالی': {
#                         'امکان حذف سوپر یوزر از طریق ای پی آی وجود ندارد': 'امکان حذف سوپر یوزر از طریق ای پی آی وجود ندارد',
#                     }
#                 },
#             }
#         }
#         return JsonResponse(json_response_body)
#
#     def post(self, request, *args, **kwargs):
#         user = AuthToken.objects.filter(token_key=token_8_first_letter(request))[0].user
#         profiles = Profile.objects.filter(user=user)
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)
#
#     def put(self, request, *args, **kwargs):
#         front_input = json.loads(request.body)
#         user = AuthToken.objects.filter(token_key=token_8_first_letter(request))[0].user
#         profile = Profile.objects.get(user=user)
#         try:
#             new_password = front_input['new_password']
#             user.set_password(new_password)
#             user.save()
#         except:
#             pass
#
#         try:
#             email = front_input['email']
#             user.email = email
#             user.save()
#         except:
#             pass
#
#         try:
#             biography = front_input['biography']
#             profile.biography = biography
#             profile.save()
#         except:
#             pass
#
#         try:
#             profile_pic_id = front_input['profile_pic_id']
#             try:
#                 image = FileGallery.objects.get(created_by=user, id=profile_pic_id)
#                 profile.profile_pic = image
#                 profile.save()
#             except:
#                 json_response_body = {
#                     'method': 'put',
#                     'request': 'ویرایش کاربر',
#                     'result': 'ناموفق',
#                     'message': 'تصویر با ایدی ارائه شده وجود ندارد'
#                 }
#                 return JsonResponse(json_response_body)
#         except:
#             pass
#         profiles = Profile.objects.filter(user=user)
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)
#
#     def delete(self, request, *args, **kwargs):
#         user = AuthToken.objects.filter(token_key=token_8_first_letter(request))[0].user
#         if user.is_superuser:
#             json_response_body = {
#                 'method': 'post',
#                 'request': 'حذف کاربر',
#                 'result': 'ناموفق',
#                 'message': 'امکان حذف سوپر یوزر از طریق ای پی آی وجود ندارد'
#             }
#             return JsonResponse(json_response_body)
#         user.delete()
#         json_response_body = {
#             'method': 'post',
#             'request': 'حذف کاربر',
#             'result': 'موفق',
#             'message': 'کاربر حذف شد'
#         }
#         return JsonResponse(json_response_body)
#
