import uuid
from django.db import models


class RawData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, null=True, blank=True)
    path = models.TextField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uploaded = models.BooleanField(default=False)

    @property
    def title(self):
        return str(self.name)
