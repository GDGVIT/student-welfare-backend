# Generated by Django 4.0.10 on 2024-04-15 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_rename_organization_event_organizing_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Description'),
        ),
    ]
