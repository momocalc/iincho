from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_POST, require_GET

from .models import Category
from django.db.models import Count


class CategoryListViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListViewMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.annotate(
            num_articles=Count('article')
        ).filter(num_articles__gt=0).order_by('name')
        return context


class CategoryListUpdateView(LoginRequiredMixin, CategoryListViewMixin, TemplateView, ProcessFormView):
    template_name = 'categories/category_list_edit.jinja2'
