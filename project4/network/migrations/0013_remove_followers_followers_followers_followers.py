# Generated by Django 4.2.6 on 2024-08-04 10:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0012_rename_blal_followers_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="followers",
            name="followers",
        ),
        migrations.AddField(
            model_name="followers",
            name="followers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
