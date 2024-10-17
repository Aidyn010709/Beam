import secrets
import string
from typing import Any

import pyotp
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from beam.abstract_models import AbstractField


class UserManager(BaseUserManager["User"]):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone: str, password: str, **extra_fields: Any) -> "User":
        """Create and save a User with the given phone_number and password."""
        if not phone:
            raise ValueError("The given phone_number must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, phone: str, password: str = None, **extra_fields: Any
    ) -> "User":
        """Create and save a regular User with the given phone_number and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(
        self, phone: str, password: str, **extra_fields: Any
    ) -> "User":
        """Create and save a SuperUser with the given phone_number and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser, AbstractField):
    password = models.CharField("password", max_length=100)
    objects = UserManager()  # type: ignore
    is_active = models.BooleanField(
        default=False,
        verbose_name="Активный",
        help_text=("Отметьте, если пользователь активный. "),
    )
    username = models.CharField("юзернейм", max_length=255, null=True, blank=True)
    email = models.EmailField("электронная почта", null=True, blank=True)
    phone = PhoneNumberField("номер телефона", unique=True, null=True, blank=True)
    first_name = models.CharField("first name", max_length=150, blank=True, null=True)
    last_name = models.CharField("last name", max_length=150, blank=True, null=True)
    fathers_name = models.CharField(
        "fathers name", max_length=150, blank=True, null=True
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "phone",
            "first_name",
        ]

    def __str__(self) -> str:
        return f"{self.phone}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def authenticate(self, otp: int) -> bool:
        t = pyotp.TOTP(self.key, interval=120)
        return t.verify(str(otp))
    