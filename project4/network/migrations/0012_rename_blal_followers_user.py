# Generated by Django 4.2.6 on 2024-08-04 09:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0011_remove_user_followers_remove_user_following_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="followers",
            old_name="blal",
            new_name="user",
        ),
    ]
