from django.conf.urls import include, url
from .views import CategoryListUpdateView

urlpatterns = [
    url(r'^list_update/$', CategoryListUpdateView.as_view(), name='list_update'),
    url(r'^move_category/$', 'categories.views.move_category', name='move_category'),
    url(r'^delete_category/$', 'categories.views.delete_category', name='delete_category'),
    url(r'^update_name/$', 'categories.views.update_name', name='update_name'),
    url(r'^merge_categories/$', 'categories.views.merge_categories', name='merge_categories'),
    url(r'^add_category/$', 'categories.views.add_category', name='add_category'),
]
