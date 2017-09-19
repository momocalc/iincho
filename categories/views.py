from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from categories import NOT_CATEGORISED
from .models import Category
from articles.models import Article
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
            ~Q(name__startswith='template/'), ~Q(name__startswith=NOT_CATEGORISED)) \
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

    new_path = new_parent + target[separate_idx + 1:]
    upd_res, msg = _update_path(target, new_path)

    return JsonResponse({'state': upd_res, 'message': msg})


@require_POST
def delete_category(request):
    """
    カテゴリ削除
    :param request:
    :return:
    """
    target = request.POST.get('target_path')  # type:str

    # 記事のcategoryの変更
    not_cat = Category.objects.get(name=NOT_CATEGORISED)
    articles = Article.objects.select_related('category').filter(category__name__startswith=target)
    articles.update(category=not_cat)

    # カテゴリ削除
    Category.objects.filter(name__startswith=target).delete()

    return JsonResponse({'state': True})


@require_POST
def update_name(request):
    """
    名称変更
    :param request:
    :return:
    """

    target = request.POST.get('target_path')  # type:str
    name = request.POST.get('name').strip()  # type:str

    is_valid, msg = _is_valid_name(name)
    if not is_valid:
        return JsonResponse({
            'state': False,
            'message': msg
        })

    separate_idx = target.rfind('/', 0, -1)
    parent = '' if separate_idx < 0 else target[:separate_idx + 1]

    new_path = parent + name + '/'
    upd_res, msg = _update_path(target, new_path)

    return JsonResponse({'state': upd_res, 'message': msg})


def _is_valid_name(name):
    if not name:
        return False, 'カテゴリ名を入力してください'
    if name.find('/') >= 0:
        return False, 'カテゴリ名に「/」は使用できません'
    if name == NOT_CATEGORISED[:-1]:
        return False, 'この名称はカテゴリ名に使用できません'

    return True, None


def _update_path(target_path, new_path):
    # 同一ディレクトリが存在する場合は、移動を許さない
    if Category.objects.filter(name__startswith=new_path):
        return False, '同じ名前のディレクトリが存在します'

    # update
    for obj in Category.objects.filter(name__startswith=target_path).all():
        obj.name = obj.name.replace(target_path, new_path)
        obj.save()

    return True, None
