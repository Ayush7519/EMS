# Generated by Django 4.2 on 2023-04-28 12:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="managers",
            name="name",
            field=models.CharField(
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
    ]
