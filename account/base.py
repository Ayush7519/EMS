from django.db import models
from rest_framework import serializers

from ems.validations import iscontactvalidator


# validation for the image fields.
def category_image_dir_path(instance, filename):
    nm = instance.user.name  # name of the user.
    img = instance.photo  # name of the image.
    ext = img.name.split(".")[-1]  # extracting the image extensions
    filename = str(nm) + "." + str(ext)
    print(filename)
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


class basemodel(models.Model):
    GENDER_TYPE = (("Male", "male"), ("Female", "female"), ("Other", "other"))

    photo = models.ImageField(
        upload_to=category_image_dir_path, blank=False, null=False
    )
    contact = models.BigIntegerField(validators=[iscontactvalidator])
    gender = models.CharField(choices=GENDER_TYPE, max_length=20, blank=False)
    province = models.CharField(max_length=100, blank=False)
    district = models.CharField(max_length=100, blank=False)
    municipality = models.CharField(max_length=100, blank=False)
    ward = models.IntegerField(blank=False)

    class Meta:
        abstract = True
