import uuid

from django.db import models


class AbstractField(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, db_index=True
    )

    objects = models.Manager()

    class Meta:
        abstract = True
