# Generated by Django 4.0.10 on 2024-03-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_event_event_coordinators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotlight',
            name='hightlight_type',
            field=models.CharField(choices=[('alert', 'Alert'), ('event', 'Event')], default='event', max_length=50),
        ),
    ]