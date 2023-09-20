from rest_framework import serializers

from .models import Sponser,Event


# Sponser
# creating serializer for the sponser.
class Sponser_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sponser
        fields = "__all__"

#Event
#creating serializer for the event.
class Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields="__all__"
