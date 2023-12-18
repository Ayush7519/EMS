# Generated by Django 4.2 on 2023-12-07 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("emsadmin", "0007_alter_sponser_photo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveBigIntegerField(default=1)),
                ("price", models.PositiveBigIntegerField()),
                ("total_price", models.PositiveBigIntegerField()),
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="emsadmin.event"
                    ),
                ),
            ],
        ),
    ]