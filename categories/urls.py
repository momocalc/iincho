from django.conf.urls import include, url
from .views import CategoryListUpdateView

urlpatterns = [
    url(r'^list_update/$', CategoryListUpdateView.as_view(), name='list_update'),
    url(r'^move_category/$', 'categories.views.move_category', name='move_category'),
    url(r'^delete_category/$', 'categories.views.delete_category', name='delete_category'),
]
