from datetime import datetime

from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.renders import UserRenderer
from account.utils import Util
from booking.serializer import (
    TicketCreateSerializer,
    UserBookedTicket_Serializer,
)

from .models import Event, Ticket

# Create your views here.


# creating the view for the ticket api.
class TicketCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id, *args, **kwargs):
        try:
            event_data = Event.objects.get(id=event_id)
            rcp = event_data.remaining_capacity
        except Event.DoesNotExist:
            return Response(
                {
                    "msg": f"Oops we dont have any event with this id: {event_id}"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        current_date_time = datetime.now()
        # converting the datetime into str.
        timestamp_str = current_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        # removing the - : from the data.
        formatted_timestamp = (
            timestamp_str.replace("-", "")
            .replace(":", "")
            .replace(".", "")
            .replace(" ", "")
        )
        # making the ticket number.
        ticket_number = "TKT" + str(formatted_timestamp)
        serializer = TicketCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data["booked_by"] = request.user
            serializer.validated_data["ticket_num"] = ticket_number
            qtn = serializer.validated_data["quantity"]
            # calculating the remaining capacity.
            if qtn > rcp:
                return Response(
                    {"msg": f"Sorry {qtn} tickets are not available...!!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                rm_ticket = rcp - qtn
                print(rm_ticket)
                event_data.remaining_capacity = rm_ticket
                event_data.save()
            serializer.save()
            user = request.user
            # data for the front-end
            fdata = serializer.data
            # rendering the template in the api.
            email_content = render_to_string("ticket.html", {"ticket": fdata})
            data = {
                "subject": "Your Ticket Booking Have Been Sucesfully Booked",
                "to_email": user.email,
                "html_message": email_content,
            }
            Util.send_email1(data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


# login user profile part for the history of the ticket booking.
class UserBookedTicketApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserBookedTicket_Serializer

    def get_queryset(self):
        user = self.request.user
        query = Ticket.objects.filter(booked_by=user).order_by(
            "-ticket_id"
        )  # here time and date is needed.
        return query

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"msg": "Oops! You Have Not Booked Any Event...!!!"},
                status=status.HTTP_404_NOT_FOUND,
            )
