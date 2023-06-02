from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # user login path.
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user registration path",
    ),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="user login path",
    ),
    path(
        "user-profile/",
        views.UserProfileView.as_view(),
        name="user profile details view path",
    ),
    path(
        "user-profile-update/<int:pk>/",
        views.UserProfileUpdateView.as_view(),
        name="user profile update path",
    ),
    path(
        "password-change/",
        views.UserPasswordChangeView.as_view(),
        name="user password change path",
    ),
    path(
        "send-reset-password-email/",
        views.SendPassowrdEmailView.as_view(),
        name="password change email path",
    ),
    path(
        "reset-password/<uid>/<token>/",
        views.UserPasswordResetView.as_view(),
        name="user e-password change path",
    ),
    # artist path
    path(
        "artist/create/",
        views.ArtistCreateApiView.as_view(),
        name="artist create path",
    ),
    path(
        "artist/list/",
        views.ArtistListApiView.as_view(),
        name="artist list path",
    ),
    path(
        "artist/search/",
        views.ArtistSearchApiViews.as_view(),
        name="artist search path",
    ),
    path(
        "artist/update/<int:pk>/",
        views.ArtistUpdateView.as_view(),
        name="artist update path",
    ),
    path(
        "artist/delete/<int:pk>/",
        views.ArtistDeleteView.as_view(),
        name="artist delete path",
    ),
    # normal user path
    path(
        "normal-user/create/",
        views.NormalUserCreateApiView().as_view(),
        name="normal user create path",
    ),
    path(
        "normal-user/list/",
        views.NormalUserListApiView.as_view(),
        name="normal user list path",
    ),
    path(
        "normal-user/search/",
        views.NormalUserSearchApiViews.as_view(),
        name="normal user search path",
    ),
    path(
        "normal-user/update/<int:pk>/",
        views.NormalUserUpdateApiView.as_view(),
        name="normal user update path",
    ),
    path(
        "normal-user/delete/<int:pk>/",
        views.NormalUserDeleteApiView.as_view(),
        name="normal user delete path",
    ),
    # manager path
    path(
        "manager/create/",
        views.ManagerCreateApiViews.as_view(),
        name="manager create path",
    ),
    path(
        "manager/list/",
        views.ManagerListApiViews.as_view(),
        name="manager list path",
    ),
    path(
        "manager/search/",
        views.ManagerSearchApiViews.as_view(),
        name="manager search path",
    ),
    path(
        "manager/update/<int:pk>/",
        views.ManagerUpdateApiViews.as_view(),
        name="manager update path",
    ),
    path(
        "manager/delete/<int:pk>/",
        views.ManagerDeleteApiViews.as_view(),
        name="manager delete path",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
