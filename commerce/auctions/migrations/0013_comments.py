# Generated by Django 4.2.6 on 2024-07-19 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0012_alter_bid_bid_alter_listings_starting_bid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment", models.CharField(max_length=600)),
                (
                    "listing",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="auctions.listings",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
