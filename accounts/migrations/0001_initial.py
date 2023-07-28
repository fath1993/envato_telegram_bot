# Generated by Django 4.2.1 on 2023-06-01 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckSmsValidity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, verbose_name='شماره موبایل')),
                ('pass_code', models.CharField(max_length=12, verbose_name='رمز مرتبط')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': '0 - login-check',
                'verbose_name_plural': '0 - login-check',
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biography', models.CharField(blank=True, max_length=255, null=True, verbose_name='درباره من')),
                ('is_vip', models.BooleanField(default=False, verbose_name='آیا این کاربر ویژه است؟')),
                ('profile_pic', models.ImageField(blank=True, default='../static/custom/profile.png', upload_to='', verbose_name='عکس پروفایل')),
                ('account_credit', models.PositiveIntegerField(default=0, verbose_name='اعتبار حساب')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': '1 - پروفایل',
                'verbose_name_plural': '1 - پروفایل',
            },
        ),
    ]
