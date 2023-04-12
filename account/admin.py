from django.contrib import admin

from .models import Artist, Managers, NormalUser, User


# admin registrstion of the user.
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "username",
        "date_created",
        "date_updated",
        "is_artist",
        "is_user",
        "is_active",
        "is_admin",
    )


admin.site.register(User, UserModelAdmin)


# admin registration of the artist.
class ArtistModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "type_of_the_performer",
        "performed_in",
        "description",
        "manager",
    )


admin.site.register(Artist, ArtistModelAdmin)


# admin registration of the normal-user.
class Normal_UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "photo",
        "contact",
        "gender",
        "province",
        "district",
        "municipality",
        "ward",
    )


admin.site.register(NormalUser, Normal_UserModelAdmin)


# admin registration of the manager.
class ManagerModelAdmin(admin.ModelAdmin):
    list_display = (
        "artist",
        "name",
        "email",
        "contact",
    )


admin.site.register(Managers, ManagerModelAdmin)
