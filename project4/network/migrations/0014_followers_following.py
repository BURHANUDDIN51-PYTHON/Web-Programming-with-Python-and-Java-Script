# Generated by Django 4.2.6 on 2024-08-04 10:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0013_remove_followers_followers_followers_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="followers",
            name="following",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
