from django.core.validators import RegexValidator
from django.db import models
# from django.db.models import TextChoices
from django.utils.safestring import mark_safe

from beam.abstract_models import AbstractField


class Indicator(AbstractField):
    indicator = models.CharField(
        max_length=5,
        verbose_name="Индикатор",
        unique=True,
        validators=[
            RegexValidator(
                regex="^[A-Z]+$",
                message="Enter only capital letters.",
                code="invalid_capital_letters",
            ),
        ],
    )

    class Meta:
        verbose_name = "Индикатор"
        verbose_name_plural = "Индикаторы"
        ordering = ["indicator"]

    def __str__(self):
        return self.indicator
    

class Category(AbstractField):
    network = models.ForeignKey(
        "network.Network",
        on_delete=models.SET_NULL,
        related_name="category_network",
        verbose_name="Сеть",
        null=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )
    name = models.CharField(max_length=255, verbose_name="Название подкатегории")
    photo = models.FileField(
        upload_to="category-pictures/", verbose_name="Картинка", blank=True, null=True
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
    )
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        verbose_name="Индикатор",
        related_name="category_indicator",
    )
    access_clients = models.BooleanField(default=False, verbose_name="Доступ клиентам")


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.indicator} - {self.name}"

    def photo_preview(self):
        return mark_safe(f'<img src = "{self.photo.url}" width = "300"/>')
    

class Product(AbstractField):
    network = models.ForeignKey(
        "network.Network",
        on_delete=models.SET_NULL,
        related_name="product_network",
        verbose_name="Сеть",
        null=True,
    )
    name = models.CharField(max_length=255, verbose_name="Название товара")
    photo = models.FileField(
        upload_to="product/", verbose_name="Картинка", null=True, blank=True
    )
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        verbose_name="Индикатор",
        related_name="product_indicator",
    )
    access_clients = models.BooleanField(default=False, verbose_name="Доступ клиентам")

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def photo_preview(self):
        return mark_safe(f'<img src = "{self.photo.url}" width = "300"/>')
