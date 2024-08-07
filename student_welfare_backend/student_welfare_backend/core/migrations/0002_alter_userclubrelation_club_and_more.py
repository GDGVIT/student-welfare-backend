# Generated by Django 4.0.10 on 2023-03-30 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userclubrelation",
            name="club",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_club_relations",
                to="core.club",
            ),
        ),
        migrations.AlterField(
            model_name="userclubrelation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_club_relations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
