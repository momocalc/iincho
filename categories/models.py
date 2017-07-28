from django.db import models
from core.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.TextField(unique=True)
    sort_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name
