from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "phone",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_superuser",
    ]
    list_display_links = ["phone"]
    search_fields = ["phone", "first_name", "last_name"]
    list_filter = ["is_active","is_superuser"]
    ordering = ["-created_at", "-updated_at"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


admin.site.register(User, UserAdmin)