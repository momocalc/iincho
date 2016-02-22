from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import User


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    photo = models.URLField(blank=True)
