# Generated by Django 4.2 on 2023-06-02 10:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sponser",
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
                    "sponser_type",
                    models.CharField(
                        choices=[
                            ("Title Sponser", "title sponser"),
                            ("Platinum", "platinum"),
                            ("Gold", "gold"),
                            ("Silver", "silver"),
                            ("Bronze", "bronze"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-z- A-z]+$",
                                code="Invalid name",
                                message="Invalide data to the fields........",
                            )
                        ],
                    ),
                ),
                ("amount", models.BigIntegerField()),
            ],
        ),
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
