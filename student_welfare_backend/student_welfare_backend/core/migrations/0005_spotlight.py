# Generated by Django 4.0.10 on 2024-03-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_club_name_alter_event_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spotlight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('time', models.DateTimeField()),
                ('hightlight_type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Spotlight Highlights',
                'verbose_name_plural': 'Spotlight Highlights',
            },
        ),
    ]