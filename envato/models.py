from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodel


class EnvatoFile(models.Model):
    page_link = models.CharField(max_length=2000, null=False, blank=False, verbose_name="لینک صفحه اصلی فایل")
    src_link = models.CharField(max_length=2000, null=True, blank=True, verbose_name="لینک اصلی فایل")
    file = models.FileField(upload_to='envato/', null=True, blank=True, verbose_name="فایل")
    in_progress = models.BooleanField(default=False, verbose_name='آیا در حال دانلود است؟')
    is_acceptable_file = models.BooleanField(default=True, verbose_name='آیا فایل با فرمت های طراحی شده سازگار است؟')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name="تاریخ و زمان ایجاد")
    updated_at = jmodel.jDateTimeField(auto_now=True, verbose_name="تاریخ و زمان بروزرسانی")

    class Meta:
        ordering = ['-updated_at', ]
        verbose_name = "فایل انواتو"
        verbose_name_plural = "فایل های انواتو"

    def __str__(self):
        return self.page_link


class EnvatoSetting(models.Model):
    sleep_time = models.PositiveSmallIntegerField(default=5, verbose_name="زمان توقف ربات بین هر کوئری")
    envato_user = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام کاربری انواتو')
    envato_pass = models.CharField(max_length=255, null=True, blank=True, verbose_name='کلمه عبور انواتو')
    envato_cookie = models.FileField(upload_to='envato', null=True, blank=True, verbose_name='کوکی انواتو')
    login_status = models.BooleanField(default=False, verbose_name='آیا احراز هویت فعال است؟')
    # is_proxy_on = models.BooleanField(default=True, null=False, blank=False, verbose_name='پراکسی فعال باشد؟')
    envato_thread_number = models.PositiveSmallIntegerField(default=4, null=False, blank=False, verbose_name='تعداد پردازش همزمان انواتو')
    envato_queue_number = models.PositiveSmallIntegerField(default=4, null=False, blank=False, verbose_name='تعداد پردازش صف انواتو')

    def __str__(self):
        return 'تنظیمات انواتو'

    class Meta:
        verbose_name = 'تنظیمات انواتو'
        verbose_name_plural = 'تنظیمات انواتو'


def get_envato_config_settings():
    try:
        envato_config_settings = EnvatoSetting.objects.filter().latest('id')
    except:
        envato_config_settings = EnvatoSetting(
            sleep_time=5,
        )
        envato_config_settings.save()
    return envato_config_settings


class EnvatoActiveThread(models.Model):
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ترد فعال انواتو"
        verbose_name_plural = "ترد های فعال انواتو"