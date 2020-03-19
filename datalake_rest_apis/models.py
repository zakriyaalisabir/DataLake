import uuid
from django.db import models
from .storage_backends import StaticStorage


class RawDataFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # title = models.CharField(max_length=25, null=False, blank=True)
    file = models.FileField(storage=StaticStorage())
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
