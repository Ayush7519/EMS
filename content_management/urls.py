from content_management import views
from django.urls import path

urlpatterns = [
    # content-management path
    path(
        "content-management/create/",
        views.Content_ManagementCreateApiView.as_view(),
        name="content-management create path",
    ),
    path(
        "content-management/list/",
        views.Content_ManagementListApiView.as_view(),
        name="content-management list path",
    ),
    path(
        "content-management/list/search/<str:status>/",
        views.Content_ManagementStatusListSearchApiView.as_view(),
        name="content-management based on draft path",
    ),
    path(
        "content-management/update/<int:pk>/",
        views.Content_managementUpdateApiView.as_view(),
        name="content-management update path",
    ),
    path(
        "content-management/delete/<int:pk>/",
        views.Content_ManagementDeleteApiView.as_view(),
        name="content-management delete path",
    ),
]
