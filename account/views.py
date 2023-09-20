from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.renders import UserRenderer
from ems.pagination import MyPageNumberPagination

from .models import Artist, Managers, NormalUser, User
from .serializer import Artist_Serializer  # UserDetail_Serializer,
from .serializer import (
    Alluserdelete_Serializer,
    AllUserList_Serializer,
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
    UserProfileUpdate_Serializer,
    UserRegistration_Serializer,
)
from .utils import Util


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
            # extracting the id of the registred user.
            uid = user.id
            # email sending after the user is registred and saved.
            data = {
                "subject": "Django Email",
                "body": user.name
                + " "
                + "You have been successfully registred in our Site !!!",
                "to_email": user.email,
            }
            Util.send_email(data)
            token = get_tokens_for_user(user)  # for the token...
            return Response(
                {
                    "token": token,
                    "msg": "Registration Successful",
                    "uid": uid,
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
            user_type = user.is_admin
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        "user_is_admin": user_type,
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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfile_Serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# login user profile update view.
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdate_Serializer
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(pk=user)


# login user full data update view.
# class UserLoginProfileUpdateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     renderer_classes = [UserRenderer]

#     def patch(self, request, *args, **kwargs):
#         user_id = self.request.user.pk
#         artist_id = self.request.user.artist.pk
#         user = User.objects.get(pk=user_id)
#         artist = Artist.objects.get(pk=artist_id)
#         user_data = request.data.get("user")
#         print(user_data)
#         artist_data = request.data.get("artist")
#         print(artist_data)
#         user_serializer = UserProfileUpdate_Serializer(user, data=user_data)
#         artist_serializer = Artist_Serializer(artist, data=artist_data)
#         if user_serializer.is_valid(
#             raise_exception=True
#         ) and artist_serializer.is_valid(raise_exception=True):
#             user_serializer.save()
#             artist_serializer.save()
#             return Response(
#                 {
#                     "user": user_serializer.data,
#                     "artist": artist_serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             {
#                 "user": user_serializer.errors,
#                 "artist": artist_serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# user password change view.
class UserPasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPasswordChange_Serializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password changed Sucessfully"},
                status=status.HTTP_200_OK,
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


# USERS
# all user data from the database.
class AllUserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AllUserList_Serializer
    pagination_class = MyPageNumberPagination
    permission_classes = [permissions.IsAdminUser]


# searching the user from the database.
class AllUserSearchApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AllUserList_Serializer
    filter_backends = [SearchFilter]
    search_fields = [
        "name",
        "username",
        # can add the user id in the search field if necessary.
        # "id",
        # "email",
    ]
    pagination_class = MyPageNumberPagination
    # renderer_classes = [UserRenderer]


# updating the data of the user from the admin pannel.
class AllUserUpdateApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = Alluserdelete_Serializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [UserRenderer]


# deleting the data of the user from the admin pannel.
class AllUserDeleteApiView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = Alluserdelete_Serializer
    permission_classes = [permissions.IsAdminUser]
    renderer_classes = [UserRenderer]


# Artist
# artist creating.
class ArtistCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = Artist_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ward_data = serializer.validated_data["ward"]
            if ward_data <= 0:
                return Response(
                    {"msg": "ward value cannot be 0 or less than 0"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


# artist list.
class ArtistListApiView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer_Full_Details
    pagination_class = MyPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [permissions.IsAuthenticated]


# artist update.
class ArtistUpdateView(generics.UpdateAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]


# artist delete.
class ArtistDeleteView(generics.DestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = Artist_Serializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]


# NORMAL USER
# normal user create.
class NormalUserCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = NormalUser_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ward_data = serializer.validated_data["ward"]
            if ward_data <= 0:
                return Response(
                    {"msg": "ward value cannot be 0 or less than 0"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


# normal user list.
class NormalUserListApiView(generics.ListAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer_Full_Detals
    pagination_class = MyPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [permissions.IsAuthenticated]


# normal user update.
class NormalUserUpdateApiView(generics.UpdateAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]


# normal user delete.
class NormalUserDeleteApiView(generics.DestroyAPIView):
    queryset = NormalUser.objects.all()
    serializer_class = NormalUser_Serializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]


# MANAGER
# manager create.
class ManagerCreateApiViews(generics.CreateAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer
    renderer_classes = [UserRenderer]


# managers list.
class ManagerListApiViews(generics.ListAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer_Full_Detals
    pagination_class = MyPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]


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
    permission_classes = [permissions.IsAuthenticated]


# manager update.
class ManagerUpdateApiViews(generics.UpdateAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]


# manager delete.
class ManagerDeleteApiViews(generics.DestroyAPIView):
    queryset = Managers.objects.all()
    serializer_class = Managers_Serializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]
