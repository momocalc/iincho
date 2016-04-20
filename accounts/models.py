from django.db import models
from core.models import TimeStampedModel
from django.contrib.auth.models import User


PHOTO_UPLOAD_TO = 'accounts/photo/'


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    photo = models.FileField(blank=True, upload_to=PHOTO_UPLOAD_TO)

    def __str__(self):
        return "{} [{}]".format(self.user.username,
                                self.photo.name if self.photo else 'None')