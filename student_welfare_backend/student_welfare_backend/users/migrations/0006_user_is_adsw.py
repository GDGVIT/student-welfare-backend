# Generated by Django 4.0.10 on 2024-02-11 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_otp_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_adsw',
            field=models.BooleanField(default=False, verbose_name='User is ADSW'),
        ),
    ]
