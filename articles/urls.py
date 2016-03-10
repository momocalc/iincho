from django.conf.urls import url
from .views import ArticleDetailAndCreateCommentView, ArticleCreateView, ArticleListView, ArticleUpdateView, ArticleDeleteView, OwnersArticleListView
from .views import delete_comment


urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='list'),
    url(r'^owner/(?P<owner_id>\d+)/$', OwnersArticleListView.as_view(), name='owners_articles'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailAndCreateCommentView.as_view(), name='detail'),
    url(r'^new/$', ArticleCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/edit/$', ArticleUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', ArticleDeleteView.as_view(), name='delete'),
    url(r'^(?P<article_id>\d+)/comment_delete/$', delete_comment, name='comment_delete'),
    url(r'^select_template/$',
        'articles.views.select_template', name='select_template'),
]
