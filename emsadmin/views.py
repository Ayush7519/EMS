from account.renders import UserRenderer
from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter

from ems.pagination import MyPageNumberPagination

from .models import Sponser
from .serializer import Sponser_Serializer


# Sopnser
# Sponser Creating.
class SponserCreateApiView(generics.CreateAPIView):
    queryset = Sponser.objects.all()
    serializer_class = Sponser_Serializer
    renderer_classes = [UserRenderer]


# Sponser Listing.
class SponserListApiView(generics.ListAPIView):
    queryset = Sponser.objects.all()
    serializer_class = Sponser_Serializer
    pagination_class = MyPageNumberPagination


# Sponser search.
class SponserSearchApiView(generics.ListAPIView):
    queryset = Sponser.objects.all()
    serializer_class = Sponser_Serializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "sponser_type"]
    pagination_class = MyPageNumberPagination


# Sponser update.
class SponserUpdateApiView(generics.UpdateAPIView):
    queryset = Sponser.objects.all()
    serializer_class = Sponser_Serializer
    renderer_classes = [UserRenderer]


# Sponser delete.
class SponserDeleteApiView(generics.DestroyAPIView):
    queryset = Sponser.objects.all()
    serializer_class = Sponser_Serializer
    renderer_classes = [UserRenderer]
