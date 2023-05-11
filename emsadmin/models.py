from account.models import Artist
from django.db import models

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
        choices=SPONSER_TYPE, max_length=100, null=False, blank=False
    )
    name = models.CharField(
        max_length=100, null=False, blank=False, validators=[isalphavalidator]
    )
    amount = models.BigIntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


# EVENT MODEL
class Event(models.Model):
    event_name = models.CharField(
        max_length=500, validators=[isalphanumericalvalidator], null=False, blank=False
    )
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    artist = models.OneToOneField(
        Artist, on_delete=models.CASCADE, null=False, blank=False
    )
    location = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.BigIntegerField(null=False, blank=False)
    entry_fee = models.BigIntegerField(null=False, blank=False)
    sponser = models.ForeignKey(
        Sponser, on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return self.event_name
