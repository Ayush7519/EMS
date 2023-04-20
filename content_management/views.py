from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ems.pagination import MyPageNumberPagination

from .models import Content_Management
from .serializer import Content_ManagementSerializer


# content_management
# content_management creating.
class Content_ManagementCreateApiView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = Content_ManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Content_Management.objects.update(updated_by=request.user.name)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# content-management list.
class Content_ManagementListApiView(generics.ListAPIView):
    queryset = Content_Management.objects.all()
    serializer_class = Content_ManagementSerializer
    filter_backends = [SearchFilter]
    search_fields = ["heading"]
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAdminUser]


# content-management draft list with search.
class Content_ManagementStatusListApiView(APIView, PageNumberPagination):
    permission_classes = [IsAdminUser]
    filter_backends = (SearchFilter,)
    search_fields = ["heading"]
    page_size = 10

    def get(self, request, status, format=None, *args, **kwargs):
        if status == "Draft" or status == "Publish":
            queryset = Content_Management.objects.filter(status=status)
            results = self.paginate_queryset(queryset, request, view=self)
            serializer = Content_ManagementSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        else:
            return Response(
                {"error": "Check your status.That doesn't match our status"}
            )


# content-management update.
class Content_managementUpdateApiView(generics.UpdateAPIView):
    queryset = Content_Management.objects.all()
    serializer_class = Content_ManagementSerializer
    permission_classes = [IsAdminUser]


# content-management delete.
class Content_ManagementDeleteApiView(generics.DestroyAPIView):
    queryset = Content_Management.objects.all()
    serializer_class = Content_ManagementSerializer
    permission_classes = [IsAdminUser]
