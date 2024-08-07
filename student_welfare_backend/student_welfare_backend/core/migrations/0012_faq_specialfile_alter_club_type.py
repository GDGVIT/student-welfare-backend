# Generated by Django 4.0.10 on 2024-03-17 12:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_newsletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='SpecialFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Year must be 4 digits long', regex='^\\d{4}$')])),
                ('type', models.CharField(choices=[('events', 'Events'), ('program_representatives', 'Program Representatives')], max_length=100)),
                ('file_link', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Special File',
                'verbose_name_plural': 'Special Files',
            },
        ),
        migrations.AlterField(
            model_name='club',
            name='type',
            field=models.CharField(choices=[('student_welfare', 'Student Welfare'), ('student_council', 'Student Council'), ('club', 'Club'), ('chapter', 'Chapter'), ('team', 'Team'), ('greviance_cell', 'Greviance Cell'), ('counseling_division', 'Counseling Division'), ('other', 'Other')], default='club', max_length=50, verbose_name='Type'),
        ),
    ]
