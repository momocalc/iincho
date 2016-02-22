from django.db import models
from core.fields import ContentTypeRestrictedFileField
from django.db.models.signals import post_delete
from django.dispatch import receiver

UPLOAD_TO = 'attachments'

class Attachment(models.Model):
    file = ContentTypeRestrictedFileField(
        content_type_pattern=r'^((image\/(gif|jpe?g|png))|(application\/(pdf|x-tex|postscript))|(text\/(tab-separated-values|plain|xml)))$',
        max_upload_size=5242880,
        upload_to=UPLOAD_TO)

    def __str__(self):
        return self.file.name

@receiver(post_delete, sender=Attachment)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(False)