from django.contrib.auth import get_user_model
from django.db import models

from beam.abstract_models import AbstractField

User = get_user_model()


class NetworkTypeChoices(models.TextChoices):
    service = ("furniture", "Мебель")
    carrier = ("technique", "Техника")
    branch = ("build_materials", "Стройматериал")
    company = ("company", "Продуктовая компания")


class NetworkType(models.Model):
    network_type = models.CharField(
        max_length=255,
        verbose_name="Тип сети",
        choices=NetworkTypeChoices.choices,
        default=NetworkTypeChoices.service,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.get_network_type_display()}"

    class Meta:
        verbose_name = "Тип сети"
        verbose_name_plural = "Типы сетей"
        ordering = ["network_type"]


class Network(AbstractField):
    name = models.CharField(max_length=255, verbose_name="Название Сети")
    network_type = models.ForeignKey(
        NetworkType,
        on_delete=models.PROTECT,
        verbose_name="Тип сети",
        related_name="networks_type",
        null=True,
    )
    prefix = models.CharField(max_length=2, verbose_name="Индикатор")
    logo = models.FileField(
        upload_to="logo/", blank=True, null=True, verbose_name="Логотип"
    )
    legal_address = models.CharField(
        verbose_name="Юридический Адрес", max_length=255, blank=True, null=True
    )
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="owner_network",
        verbose_name="Ответственное лицо",
        null=True,
        blank=True,
    )
    access_clients = models.BooleanField(default=False, verbose_name="Доступ клиентам")

    class Meta:
        verbose_name = "Сеть"
        verbose_name_plural = "Сети"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"