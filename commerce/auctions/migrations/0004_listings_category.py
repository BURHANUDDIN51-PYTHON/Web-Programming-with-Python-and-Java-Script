# Generated by Django 4.2.6 on 2024-07-17 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="auctions.category",
            ),
        ),
    ]
