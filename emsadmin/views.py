from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from account.renders import UserRenderer
from ems.pagination import MyPageNumberPagination

from .models import Artist, Event, Sponser
from .serializer import (
    Event_Serializer,
    EventList_Serializer,
    Sponser_Serializer,
)


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
    search_fields = [
        "name",
        "sponser_type",
    ]
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


# Event
# Event Create.
class EventCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = Event_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            artist_value = serializer.validated_data["artist"]
            print(artist_value)
            for art_data in artist_value:
                print(art_data)
                try:
                    data = Artist.objects.get(user_id=art_data.user_id)
                    data.is_available = False
                    data.save()
                except Event.DoesNotExist:
                    return Response(
                        {
                            "msg": "The Artist you have selected is not prestnt in our database"
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


# Event Complete.
class EventCompleteApiView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, event_id, *args, **kwargs):
        print(event_id)
        try:
            event_info = Event.objects.get(id=event_id)
            print(event_info)
            artists_ids = [artist.id for artist in event_info.artist.all()]

        except Event.DoesNotExist:
            return Response(
                {"msg": "Event Doesnot Exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        for art_id in artists_ids:
            # print(art_id)
            try:
                artist_info = Artist.objects.get(id=art_id)
                artist_info.is_available = True
                artist_info.save()

            except Artist.DoesNotExist:
                return Response(
                    {"msg": "Artist Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        event_info.event_completed = True
        event_info.save()

        return Response(
            {"msg": "Operation Sucessfully Completed."},
            status=status.HTTP_200_OK,
        )


# Event List.
class EventListApiView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventList_Serializer
    pagination_class = MyPageNumberPagination
    renderer_classes = [UserRenderer]


# Event Search.
# this is for the front end user so they can search the event based on their desire.
class EventSearchApiView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = Event_Serializer
    filter_backends = [SearchFilter]
    search_fields = [
        "event_name",
        "date",
        "time",
        "artist__name",
        "artist__username",
        "location",
    ]
    pagination_class = MyPageNumberPagination


# Event Delete.
class EventDeleteApiView(APIView):
    renderer_classes = [UserRenderer]

    def delete(self, request, pk, *args, **kwargs):
        try:
            event_info = Event.objects.get(id=pk)
            artists_ids = [artist.id for artist in event_info.artist.all()]

        except Event.DoesNotExist:
            return Response(
                {"msg": "Event data is not available in the database"},
                status=status.HTTP_404_NOT_FOUND,
            )

        for art_id in artists_ids:
            print(art_id)
            try:
                artist_info = Artist.objects.get(id=art_id)
                artist_info.is_available = True
                artist_info.save()

            except Artist.DoesNotExist:
                return Response(
                    {"msg": "Artist is not available."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        event_info.delete()
        return Response(
            {"msg": "Data has been sucessfully deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
