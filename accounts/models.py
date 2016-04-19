from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import User


PHOTO_UPLOAD_TO = 'accounts/'


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    photo = models.FileField(blank=True, upload_to=PHOTO_UPLOAD_TO)