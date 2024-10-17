from django.contrib import admin
from django.contrib.auth.models import Permission

from applications.network.models import Network, NetworkType

class NetworkTypeChoicesAdmin(admin.ModelAdmin): 
    model = NetworkType
    list_display = ("network_type",)
    search_fields = ("network_type",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('permissions')
        return queryset

class NetworkAdmin(admin.ModelAdmin):
    autocomplete_fields = ["owner"]
    list_display = ["network_type", "name", "owner", "legal_address"]
    list_display_links = ["network_type", "name", "owner"]
    list_filter = ["network_type"]
    search_fields = ["name"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("network_type", "owner")



admin.site.register(Network, NetworkAdmin)
admin.site.register(NetworkType, NetworkTypeChoicesAdmin)
admin.site.register(Permission)
