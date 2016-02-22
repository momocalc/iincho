from django.conf.urls import include, url
from .views import LoginView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
]
