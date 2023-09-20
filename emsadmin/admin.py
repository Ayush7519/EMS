from django.contrib import admin

from .models import Event, Sponser


# Sponser model register in the admin.
class SponserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sponser_type",
        "name",
        "amount",
    )


admin.site.register(Sponser, SponserAdmin)


# Event model register in the admin.
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event_name",
        "date",
        "time",
        "artist",
        "location",
        "capacity",
        "entry_fee",
        "sponser",
        "event_completed",
    )


admin.site.register(Event, EventAdmin)
