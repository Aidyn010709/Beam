# Generated by Django 5.1.2 on 2024-10-16 21:13

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("network", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Indicator",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_index=True, null=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_index=True, null=True),
                ),
                (
                    "indicator",
                    models.CharField(
                        max_length=5,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_capital_letters",
                                message="Enter only capital letters.",
                                regex="^[A-Z]+$",
                            )
                        ],
                        verbose_name="Индикатор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Индикатор",
                "verbose_name_plural": "Индикаторы",
                "ordering": ["indicator"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_index=True, null=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_index=True, null=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Название подкатегории"
                    ),
                ),
                (
                    "photo",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="category-pictures/",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=10,
                        null=True,
                        verbose_name="Цена",
                    ),
                ),
                (
                    "access_clients",
                    models.BooleanField(default=False, verbose_name="Доступ клиентам"),
                ),
                (
                    "network",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="category_network",
                        to="network.network",
                        verbose_name="Сеть",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="product.category",
                        verbose_name="Родительская категория",
                    ),
                ),
                (
                    "indicator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_indicator",
                        to="product.indicator",
                        verbose_name="Индикатор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_index=True, null=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, db_index=True, null=True),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название товара"),
                ),
                (
                    "photo",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="product/",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена"
                    ),
                ),
                (
                    "access_clients",
                    models.BooleanField(default=False, verbose_name="Доступ клиентам"),
                ),
                (
                    "indicator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_indicator",
                        to="product.indicator",
                        verbose_name="Индикатор",
                    ),
                ),
                (
                    "network",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_network",
                        to="network.network",
                        verbose_name="Сеть",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
                "ordering": ["name"],
            },
        ),
    ]
