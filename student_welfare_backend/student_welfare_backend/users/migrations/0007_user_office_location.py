# Generated by Django 4.0.10 on 2024-03-29 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_adsw'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='office_location',
            field=models.CharField(blank=True, max_length=255, verbose_name='Office location of the user'),
        ),
    ]