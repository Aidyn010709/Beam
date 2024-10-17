from django.contrib import admin
from django.utils.html import format_html

from applications.product.models import Category, Indicator, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin[Category]):
    def photo_tag(self, obj):
        return format_html(
            f'<img src="{obj.photo.url}" style="max-width:50px; max-height:50px"/>'
            if obj.photo
            else ""
        )

    list_display = ["parent", "name", "price", "indicator", "photo_tag"]
    list_display_links = ["parent", "name", "indicator", "photo_tag"]
    readonly_fields = ("photo_preview",)
    list_filter = ("parent",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin[Product]):
    def photo_tag(self, obj):
        return format_html(
            f'<img src="{obj.photo.url}" style="max-width:50px; max-height:50px"/>'
            if obj.photo
            else ""
        )

    list_display = ["network", "name", "price", "indicator", "photo_tag"]
    list_display_links = ["name", "indicator", "photo_tag"]
    readonly_fields = ("photo_preview",)
    list_filter = ("network",)
    search_fields = ("name",)

class IndicatorAdmin(admin.ModelAdmin):
    model = Indicator
    list_display = ("indicator",)


admin.site.register(Indicator, IndicatorAdmin)
