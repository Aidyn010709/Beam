from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Category, Product


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ("network", "access_clients")

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ("network", "access_clients")