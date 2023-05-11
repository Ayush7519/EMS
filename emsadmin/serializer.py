from rest_framework import serializers

from .models import Sponser


# Sponser
# creating serializer for the sponser.
class Sponser_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sponser
        fields = "__all__"
