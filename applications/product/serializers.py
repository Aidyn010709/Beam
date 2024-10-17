from django.db import transaction
from rest_framework import serializers

from applications.product.models import Category, Product, Indicator


def validate_only_capital_letters(value):
    if not value.isalpha() or not value.isupper():
        raise serializers.ValidationError("Enter only capital letters.")
    

class CategorySerializer(serializers.ModelSerializer):
    indicator = serializers.CharField(
        required=True,
        min_length=2,
        max_length=5,
        validators=[validate_only_capital_letters],
    )

    class Meta:
        model = Category
        fields = "__all__"

    def validate_indicator(self, indicator):
        indicator, _ = Indicator.objects.get_or_create(indicator=indicator)
        if self.instance:
            if (
                Category.objects.filter(indicator=indicator)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise serializers.ValidationError("Indicator already exists")
        elif Category.objects.filter(indicator=indicator).exists():
            raise serializers.ValidationError("Indicator already exists")
        return indicator

    def create(self, validated_data):
        with transaction.atomic():
            indicator_data = validated_data.pop("indicator", None)
            indicator = None

            if indicator_data is not None:
                indicator, created = Indicator.objects.get_or_create(
                    indicator=indicator_data
                )
            product = Category.objects.create(indicator=indicator, **validated_data)
            return product


class ProductSerializer(serializers.ModelSerializer):
    indicator = serializers.CharField(
        required=True,
        min_length=2,
        max_length=5,
        validators=[validate_only_capital_letters],
    )

    class Meta:
        model = Product
        fields = "__all__"

    def validate_indicator(self, indicator):
        indicator, _ = Indicator.objects.get_or_create(indicator=indicator)
        if self.instance:
            if (
                Product.objects.filter(indicator=indicator)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise serializers.ValidationError("Indicator already exists")
        elif Product.objects.filter(indicator=indicator).exists():
            raise serializers.ValidationError("Indicator already exists")
        return indicator

    def create(self, validated_data):
        with transaction.atomic():
            indicator_data = validated_data.pop("indicator")
            indicator = None

            if indicator_data is not None:
                indicator, created = Indicator.objects.get_or_create(
                    indicator=indicator_data
                )
            product = Product.objects.create(indicator=indicator, **validated_data)
            return product
