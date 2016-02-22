from django.db.models import Prefetch
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from braces.views import LoginRequiredMixin
from categories.views import CategoryListViewMixin
from articles.models import Article


class IndexView(CategoryListViewMixin, LoginRequiredMixin, ListView):
    template_name = 'web/index.jinja2'
    paginate_by = 10

    def __get_path_from_request(self):
        path = self.request.GET.get('path')
        if path:
            if not path.endswith('/'):
                path += '/'

        return path

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['path'] = self.__get_path_from_request()

        return context

    def get_queryset(self):
        path = self.__get_path_from_request()
        if path:
            q = Article.objects.filter(category__name__istartswith=path).order_by('-modified').select_related('owner__profile', 'category')
        else:
            q = Article.objects.order_by('-created').select_related('owner__profile', 'category')[:20]

        return q.prefetch_related(Prefetch("tag_set", to_attr="tags"))
