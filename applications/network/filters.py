import django_filters

from applications.network.models import Network


class NetworkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    partners = django_filters.UUIDFilter(method="filter_partners")

    class Meta:
        model = Network
        fields = ["network_type", "name", "access_clients"]

