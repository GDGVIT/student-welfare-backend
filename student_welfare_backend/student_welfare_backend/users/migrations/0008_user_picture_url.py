# Generated by Django 4.0.10 on 2024-04-12 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_office_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture_url',
            field=models.URLField(blank=True, verbose_name="URL of the user's profile picture"),
        ),
    ]
