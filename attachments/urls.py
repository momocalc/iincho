from django.conf.urls import url
from .views import upload_file
from django.conf import settings

urlpatterns = []

if not settings.DEMO:
    urlpatterns.append(url(r'^upload_jq$','attachments.views.upload_file_jq', name='upload_file_jq'))
