from django.contrib import admin
from applications.payment.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "total_price", "created_at", "is_verified", "is_paid"]
    list_display_links = ["id", "author", "total_price", "created_at", "is_verified", "is_paid"]
    search_fields = ["author__phone", "user__first_name", "author__last_name"]
    list_filter = ["is_verified", "is_paid"]
    ordering = ["-created_at"]
    raw_id_fields = ["author", "cart"]

admin.site.register(Order, OrderAdmin)