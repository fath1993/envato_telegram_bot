from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodel


class EnvatoFile(models.Model):
    link = models.CharField(max_length=2000, null=False, blank=False, verbose_name="لینک صفحه اصلی فایل")
    file = models.FileField(upload_to='envato-files', null=True, blank=True, verbose_name="فایل")
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name="تاریخ و زمان ایجاد")
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name="تاریخ و زمان بروزرسانی")

    class Meta:
        ordering = ['-updated_at', ]
        verbose_name = "فایل انواتو"
        verbose_name_plural = "فایل های انواتو"

    def __str__(self):
        return self.link


class EnvatoUserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    file = models.ForeignKey(EnvatoFile, on_delete=models.CASCADE, null=False, blank=False, verbose_name='فایل')
    is_single_pay = models.BooleanField(default=False, null=False, blank=False, verbose_name='آیا پرداخت تکی است؟')
    is_noticed = models.BooleanField(default=False, null=False, blank=False, verbose_name='آیا اطلاع رسانی شده است؟')


    class Meta:
        verbose_name = "ارتباط کابر و فایل"
        verbose_name_plural = "ارتباط کاربران و فایل ها"

    def __str__(self):
        return self.user.username + " | " + self.file.link


class ConfigSetting(models.Model):
    sleep_time = models.PositiveSmallIntegerField(default=60, verbose_name="زمان توقف ربات بین هر کوئری")
    envato_user = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام کاربری انواتو')
    envato_pass = models.CharField(max_length=255, null=True, blank=True, verbose_name='کلمه عبور انواتو')
    envato_cookie = models.FileField(upload_to='envato', null=True, blank=True, verbose_name='کوکی انواتو')
    # is_proxy_on = models.BooleanField(default=True, null=False, blank=False, verbose_name='پراکسی فعال باشد؟')

    def __str__(self):
        return str('تنظیمات')

    class Meta:
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"


def config_settings():
    try:
        settings = ConfigSetting.objects.filter().latest('id')
    except:
        settings = ConfigSetting(
            sleep_time=40,
        )
        settings.save()
    return settings
