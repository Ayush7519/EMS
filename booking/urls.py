from django.urls import path

from . import views

urlpatterns = [
    path(
        "ticket/booking/<int:event_id>/",
        views.TicketCreateApiView.as_view(),
        name="ticket booking path",
    ),
    path(
        "userbooked/ticket/",
        views.UserBookedTicketApiView.as_view(),
        name="path to get the ticket or event that user have booked or bought",
    ),
    path("grpah/", views.GraphAPI.as_view()),
]
