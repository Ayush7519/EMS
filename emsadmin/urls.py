from django.urls import path
from emsadmin import views

urlpatterns = [
    path(
        "sponser/create/",
        views.SponserCreateApiView.as_view(),
        name="sponser create path",
    ),
    path(
        "sponser/list/",
        views.SponserListApiView.as_view(),
        name="sponser details list path",
    ),
    path(
        "sponser/search/",
        views.SponserSearchApiView.as_view(),
        name="sponser search path",
    ),
    path(
        "sponser/update/<int:pk>/",
        views.SponserUpdateApiView.as_view(),
        name="sponser update path",
    ),
    path(
        "sponser/delete/<int:pk>/",
        views.SponserDeleteApiView.as_view(),
        name="sponser delete path",
    ),
]
