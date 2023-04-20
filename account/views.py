from account.renders import UserRenderer
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ems.pagination import MyPageNumberPagination

from .models import Artist, Managers, NormalUser, User
from .serializer import (
    Artist_Serializer,
    Artist_Serializer_Full_Details,
    Managers_Serializer,
    Managers_Serializer_Full_Detals,
    NormalUser_Serializer,
    NormalUser_Serializer_Full_Detals,
    SendPasswordEmail_Serializer,
    UserLogin_Serializer,
    UserPasswordChange_Serializer,
    UserPasswordReset_Serializer,
    UserProfile_Serializer,
    UserRegistration_Serializer,
)


# generating the token for the user.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# user registration view.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistration_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)  # for the token...
            return Response(
                {
                    "token": token,
                    "msg": "Registration Successful",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user login view.
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        "msg": "Login Successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "Email or Password is not valide"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login user profile view.
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfile_Serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# user password change view.
class UserPasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPasswordChange_Serializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password changed Sucessfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# sending the email to the user to change the password.
class SendPassowrdEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordEmail_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Passwoed Reset link send. Please check your Email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user password change view through the mail.
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordReset_Serializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Reset Sucessfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Artist
# artist creating.
class ArtistCreateApiView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer


# artist list.
class ArtistListApiView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer_Full_Details
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated]


# artist search.
class ArtistSearchApiViews(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer_Full_Details
    filter_backends = [SearchFilter]
    search_fields = [
        "user__name",
        "user__username",
    ]  # relation ma aako field lai search field ma hanlna lai chai yestari garna parxa.
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated]


# artist update.
class ArtistUpdateView(generics.UpdateAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer
    permission_classes = [IsAuthenticated]


# artist delete.
class ArtistDeleteView(generics.DestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer
    permission_classes = [IsAuthenticated]


# NORMAL USER
# normal user create.
class NormalUserCreateApiView(generics.CreateAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer


# normal user list.
class NormalUserListApiView(generics.ListAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer_Full_Detals
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated]


# normal user search.
class NormalUserSearchApiViews(generics.ListAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer_Full_Detals
    filter_backends = [SearchFilter]
    search_fields = [
        "user__name",
        "user__username",
    ]
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated]


# normal user update.
class NormalUserUpdateApiView(generics.UpdateAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer
    permission_classes = [IsAuthenticated]


# normal user delete.
class NormalUserDeleteApiView(generics.DestroyAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer
    permission_classes = [IsAuthenticated]


# MANAGER
# manager create.
class ManagerCreateApiViews(generics.CreateAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer


# managers list.
class ManagerListApiViews(generics.ListAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer_Full_Detals
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated]


# manager search.
class ManagerSearchApiViews(generics.ListAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer_Full_Detals
    filter_backends = [SearchFilter]
    search_fields = [
        "name",
        "artist__user__name",
        "artist__user__username",
    ]
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated]


# manager update.
class ManagerUpdateApiViews(generics.UpdateAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer
    permission_classes = [IsAuthenticated]


# manager delete.
class ManagerDeleteApiViews(generics.DestroyAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer
    permission_classes = [IsAuthenticated]
