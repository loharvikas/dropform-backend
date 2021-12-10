from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "is_staff",
        "date_joined",
        "last_modified_date",
    )
    list_display_links = (
        "id",
        "full_name",
        "email",
    )
    search_fields = (
        "full_name",
        "email",
    )
    list_per_page = 25


admin.site.register(User, UserAdmin)
