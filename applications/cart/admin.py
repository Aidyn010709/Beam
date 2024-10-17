from django.contrib import admin
from applications.cart.models import Cart, CartProduct


class CartProductInline(admin.TabularInline):
    model = CartProduct


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    list_display_links = ["id", "user"]
    search_fields = ["user__phone", "user__first_name", "user__last_name"]
    list_filter = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    inlines = [CartProductInline]

admin.site.register(Cart, CartAdmin)
