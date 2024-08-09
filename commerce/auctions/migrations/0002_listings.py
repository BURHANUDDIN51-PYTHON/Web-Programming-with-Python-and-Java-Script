# Generated by Django 4.2.6 on 2024-07-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="listings",
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
                ("title", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=100)),
                ("starting_bid", models.IntegerField()),
                ("url", models.CharField(blank=True, max_length=600)),
            ],
        ),
    ]
