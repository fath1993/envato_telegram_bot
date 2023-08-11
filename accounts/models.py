from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel

from envato.models import EnvatoFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    user_telegram_phone_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='شماره تماس اکانت تلگرام')
    profile_pic = models.ImageField(null=True, blank=True, verbose_name='عکس پروفایل')
    vip_expiry_date = jmodel.jDateTimeField(null=True, blank=True, verbose_name='تاریخ پایان اشتراک ویژه')
    account_credit = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name='اعتبار حساب')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class UserRequestHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='کاربر')
    file = models.ForeignKey(EnvatoFile, on_delete=models.CASCADE, null=False, blank=False, verbose_name='فایل')
    is_single_pay = models.BooleanField(default=False, null=False, blank=False, verbose_name='آیا پرداخت تکی است؟')
    is_noticed = models.BooleanField(default=False, null=False, blank=False, verbose_name='آیا اطلاع رسانی شده است؟')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name="تاریخ و زمان درخواست")

    def __str__(self):
        return self.user.username + " | " + str(self.created_at.date())

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'تاریخچه درخواست'
        verbose_name_plural = 'تاریخچه درخواست ها'