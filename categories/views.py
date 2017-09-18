from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from categories import NOT_CATEGORISED
from .models import Category
from django.db.models import Count, Q


class CategoryListViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListViewMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.annotate(
            num_articles=Count('article')
        ).filter(num_articles__gt=0).order_by('name')
        return context


class CategoryListUpdateView(LoginRequiredMixin, TemplateView, ProcessFormView):
    def get_context_data(self, **kwargs):
        context = super(CategoryListUpdateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(
            ~Q(name__startswith='template/'), ~Q(name__startswith=NOT_CATEGORISED))\
            .annotate(num_articles=Count('article')
        ).order_by('name')
        return context

    template_name = 'categories/category_edit.jinja2'


@require_POST
def move_category(request):
    """
    カテゴリの移動
    postパラメータ"target_path"のカテゴリを"new_parent_path"の配下に移動する
    :param request:
    :return: dictionary(state: true/false, message: error message)
    """
    target = request.POST.get('target_path')  # type:str
    new_parent = request.POST.get('new_parent_path')  # type:str
    separate_idx = target.rfind('/', 0, -1)

    def is_valid_input():
        if new_parent != '' and not new_parent.endswith('/'):
            return False
        if new_parent and new_parent.startswith(target):
            return False

        return True

    if not is_valid_input():
        return JsonResponse({
            'state': False,
            'message': 'この移動はできません'
        })

    new_name = new_parent + target[separate_idx + 1:]
    # 同一ディレクトリが存在する場合は、移動を許さない
    if Category.objects.filter(name__startswith=new_name):
        return JsonResponse({
            'state': False,
            'message': '同じ名前のディレクトリが存在します'
        })

    # update
    for obj in Category.objects.filter(name__startswith=target).all():
        obj.name = obj.name.replace(target, new_name)
        obj.save()

    return JsonResponse({'state': True})
