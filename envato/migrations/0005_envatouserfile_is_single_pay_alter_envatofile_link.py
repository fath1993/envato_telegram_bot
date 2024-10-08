# Generated by Django 4.2.3 on 2023-07-27 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('envato', '0004_envatofile_envatouserfile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='envatouserfile',
            name='is_single_pay',
            field=models.BooleanField(default=False, verbose_name='آیا پرداخت تکی است؟'),
        ),
        migrations.AlterField(
            model_name='envatofile',
            name='link',
            field=models.CharField(max_length=2000, verbose_name='لینک صفحه اصلی فایل'),
        ),
    ]
