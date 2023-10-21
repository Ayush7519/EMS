from django.db import models
from rest_framework import serializers

from account.models import Artist
from ems.validations import isalphanumericalvalidator, isalphavalidator


# SPONSER MODEL
class Sponser(models.Model):
    SPONSER_TYPE = (
        ("Title Sponser", "title sponser"),
        ("Platinum", "platinum"),
        ("Gold", "gold"),
        ("Silver", "silver"),
        ("Bronze", "bronze"),
    )
    sponser_type = models.CharField(
        choices=SPONSER_TYPE,
        max_length=100,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[isalphavalidator],
    )
    amount = models.BigIntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


# this is for validating the image.
def category_image_dir_path(instance, filename):
    event_name = instance.event_name
    img = instance.photo  # name of the image.
    ext = img.name.split(".")[-1]  # extracting the image extensions
    filename = str(event_name) + "." + str(ext)
    # print(filename)
    # validating the image extension.
    if (
        str(ext).lower() == "png"
        or str(ext).lower() == "jpg"
        or str(ext).lower() == "jpeg"
    ):
        return filename
    else:
        raise serializers.ValidationError(
            "Extension Doesnot match.It should be of png,jpg,jpeg"
        )


# EVENT MODEL
class Event(models.Model):
    photo = models.ImageField(
        upload_to=category_image_dir_path,
        blank=False,
        null=False,
    )
    event_name = models.CharField(
        max_length=500,
        validators=[isalphanumericalvalidator],
        null=False,
        blank=False,
    )
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    # this is the place to change in the host api.
    artist = models.ManyToManyField(
        Artist,
    )
    location = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.BigIntegerField(null=False, blank=False)
    entry_fee = models.BigIntegerField(null=False, blank=False)
    sponser = models.ManyToManyField(Sponser, blank=True, null=True)
    event_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name
