# Generated by Django 4.2 on 2023-05-02 11:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_alter_managers_name"),
        ("emsadmin", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                (
                    "event_name",
                    models.CharField(
                        max_length=500,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-z- A-z 0-9]+$",
                                code="Invalide name",
                                message="Invalide data to the fields......",
                            )
                        ],
                    ),
                ),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("location", models.CharField(max_length=100)),
                ("capacity", models.BigIntegerField()),
                ("entry_fee", models.BigIntegerField()),
                (
                    "artist",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="account.artist"
                    ),
                ),
                (
                    "sponser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="emsadmin.sponser",
                    ),
                ),
            ],
        ),
    ]