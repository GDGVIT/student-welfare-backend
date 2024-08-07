# Generated by Django 4.0.10 on 2024-04-28 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_organization_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.CharField(choices=[('student_welfare', 'Student Welfare'), ('student_council', 'Student Council'), ('club', 'Club'), ('chapter', 'Chapter'), ('team', 'Team'), ('greviance_cell', 'Greviance Cell'), ('counselling_division', 'Counselling Division'), ('other', 'Other')], default='club', max_length=50, verbose_name='Type'),
        ),
    ]
