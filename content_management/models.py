from django.db import models

from ems.validations import isalphavalidator


class Content_Management(models.Model):
    STATUS_CHOICES = (
        ("Draft", "draft"),
        ("Publish", "publish"),
    )
    HEADING_CHOICES = (
        ("Home", "home"),
        ("About", "about"),
        ("Blog", "blog"),
    )
    heading = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        validators=[isalphavalidator],
        choices=HEADING_CHOICES,
    )
    content = models.TextField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)

    def __str__(self):
        return self.heading
