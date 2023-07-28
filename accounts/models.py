from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel


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
