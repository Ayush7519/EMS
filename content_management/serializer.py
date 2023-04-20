from rest_framework import serializers

from .models import Content_Management


# Content_management
# creating the serializer for the content_management.
class Content_ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_Management
        fields = "__all__"
