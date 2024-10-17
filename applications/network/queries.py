from applications.network.models import Network

network_query = (
    Network.objects.select_related("owner")
    .only(
        "id",
        "name",
        "network_type",
        "logo",
        "owner",
        "legal_address",
    )
)
