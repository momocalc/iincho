from .models import Category
from django.db.models import Count


class CategoryListViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListViewMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.annotate(
            num_articles=Count('article')
        ).filter(num_articles__gt=0).order_by('name')
        return context
