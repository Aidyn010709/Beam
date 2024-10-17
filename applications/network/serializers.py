from rest_framework import serializers

from applications.product.models import Category, Product
from applications.network.models import Network, NetworkType
from .services import NetworkService

class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = "__all__"

    def create(self, validated_data):
        return NetworkService.create_network(
            self.context.get("request"), validated_data
        )

    def update(self, instance, validated_data):
        return NetworkService.update_network(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class NetworkListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = [
            "id",
            "name",
            "network_type",
            "owner",
            "access_clients",
        ]


class NetworkDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
    