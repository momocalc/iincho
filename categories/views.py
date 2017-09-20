from braces.views import StaffuserRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from categories import NOT_CATEGORISED
from .models import Category
from articles.models import Article
from django.db.models import Count, Q
from .validation import validation_name, validation_unique_path


class CategoryListViewMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListViewMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.annotate(
            num_articles=Count('article')
        ).filter(num_articles__gt=0).order_by('name')
        return context


class CategoryListUpdateView(StaffuserRequiredMixin, TemplateView, ProcessFormView):
    """
    カテゴリ管理画面View
    formは、統合処理でのみ使用。 他はajaxで処理する。
    """

    def get_context_data(self, **kwargs):
        context = super(CategoryListUpdateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(
            ~Q(name__startswith='template/'), ~Q(name__startswith=NOT_CATEGORISED)) \
            .annotate(num_articles=Count('article')).order_by('name')
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
    try:
        validation_unique_path(new_path)
        _update_path(target, new_path)
        return JsonResponse({'state': True})
    except AttributeError as e:
        return JsonResponse({'state': False, 'message': str(e)})


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

    try:
        validation_name(name)

        separate_idx = target.rfind('/', 0, -1)
        parent = '' if separate_idx < 0 else target[:separate_idx + 1]
        new_path = parent + name + '/'

        validation_unique_path(new_path)

        _update_path(target, new_path)
        return JsonResponse({'state': True})
    except AttributeError as e:
        return JsonResponse({'state': False, 'message': str(e)})


@require_POST
def merge_categories(request):
    """
    カテゴリの統合
    統合後のカテゴリはルート直下に配置し、統合前のカテゴリは削除する
    :param request:
    :return:
    """

    target_paths = request.POST.getlist('target_paths[]')
    name = request.POST.get('name')

    try:
        new_category_path = name + '/'
        validation_name(name)
        validation_unique_path(new_category_path)

        new_category = Category.objects.create(name=new_category_path)
        for path in target_paths:
            category = Category.objects.filter(name__exact=path)
            if category:
                articles = Article.objects.filter(category=category)
                articles.update(category=new_category)
                category.delete()

    except AttributeError as e:
        return JsonResponse({'state': False, 'message': str(e)})

    return JsonResponse({'state': True})


@require_POST
def add_category(request):
    """
    カテゴリ追加
    :param request:
    :return:
    """

    parent = request.POST.get('parent')  # type:str
    name = request.POST.get('name').strip()  # type:str

    try:
        validation_name(name)
        new_path = parent + name + '/'
        validation_unique_path(new_path)
        Category.objects.create(name=new_path)

        return JsonResponse({'state': True})
    except AttributeError as e:
        return JsonResponse({'state': False, 'message': str(e)})


def _update_path(target_path, new_path):
    # update
    for obj in Category.objects.filter(name__startswith=target_path).all():
        obj.name = obj.name.replace(target_path, new_path)
        obj.save()
