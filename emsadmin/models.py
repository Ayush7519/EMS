from django.db import models

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


# EVENT MODEL
class Event(models.Model):
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
    sponser = models.ManyToManyField(
        Sponser,
    )
    event_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name
