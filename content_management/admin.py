from django.contrib import admin

from .models import Content_Management


# admin registrstion of the contant_management.
class Content_ManagementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "heading",
        "content",
        "date_created",
        "date_updated",
        "updated_by",
        "status",
    )


admin.site.register(Content_Management, Content_ManagementAdmin)
