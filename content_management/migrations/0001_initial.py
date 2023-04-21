# Generated by Django 4.2 on 2023-04-20 06:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Content_Management",
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
                    "heading",
                    models.CharField(
                        max_length=50,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[a-z- A-z]+$",
                                code="Invalid name",
                                message="Invalide data to the fields........",
                            )
                        ],
                    ),
                ),
                ("content", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("updated_by", models.CharField(max_length=10)),
                (
                    "status",
                    models.CharField(
                        choices=[("Draft", "draft"), ("Publish", "publish")],
                        max_length=100,
                    ),
                ),
            ],
        ),
    ]