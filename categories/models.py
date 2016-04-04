from django.db import models
from core.models import TimeStampedModel

# Create your models here.


class Category(TimeStampedModel):
    name = models.TextField(unique=True)
    sort_number = models.IntegerField(default=0)
