from django.db.models import QuerySet
from django.contrib.auth import get_user_model

User = get_user_model()
# from boomerang_post.statuses import StatusChoices

from applications.network.models import Network, NetworkType, NetworkTypeChoices


class NetworkService:

    @classmethod
    def create_network(cls, request, data: dict) -> Network:
        data.pop("logo", None)
        logo = request.FILES.get("logo")
        network = Network.objects.create(**data, logo=logo)
        network.save()
        return network

    @staticmethod
    def update_network(instance, data: dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
