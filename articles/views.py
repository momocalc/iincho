from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.http import require_POST,require_GET
from .models import Article, Comment, Tag
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import ArticleForm, CommentForm
from braces.views import LoginRequiredMixin
from categories.models import Category
from categories.views import CategoryListViewMixin
import re
from django.db.models import Q, Prefetch
from core.mixins import TagSearchMixin, CategorySearchMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
import categories
from .utils import rebuild_edit_title, rebuild_edit_title_without_template_prefix, template_formatting

class ArticleSearchMixin(object):

    def get_queryset(self):

        queryset = super(ArticleSearchMixin, self).get_queryset()
        if hasattr(self, 'query'):
            q = self.query
        else:
            q = self.request.GET.get('query')

        if not q:
            return queryset

        for word in [x for x in re.split(r'\s+', q) if x]:
            queryset = queryset.filter(
                Q(title__contains=word) | Q(body__contains=word))

        return queryset


class SetTagsAndCategorizeMixin(object):

    def __get_category(self, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return Category.objects.create(name=name)

    def __split_category(self, str):
        text = re.sub(r'/*\s*/\s*', '/', str.strip())
        last_slash = text.rfind('/')

        if last_slash < 1:
            category = categories.NOT_CATEGORISED
        else:
            category = text[:last_slash+1]
            if not category.startswith('/'):
                category = '/' + category

        if last_slash+1 >= len(text):
            other_text = None
        else:
            other_text = text[last_slash+1:].strip()

        return category, other_text

    def __split_tags(self, str):
        first_hash = str.find('#')
        if first_hash < 0 or first_hash == len(str) - 1:
            return str, None

        title = str[:first_hash].strip()
        tags = set([x for x in re.split('[\s,#]+', str[first_hash:]) if x and len(x) <= 100])
        return title, tags

    def __split(self, inputted_title):
        title = None
        tags = None

        category, str = self.__split_category(inputted_title)
        if str:
            title, tags = self.__split_tags(str)

        title = title or 'no title'

        return category, title, tags

    def __create_tags(self, article, tags):
        # delete and insert
        Tag.objects.filter(article=article).delete()
        if not tags:
            return

        for tag in tags:
            Tag.objects.create(article=article, name=tag)

    def form_valid(self, form):
        obj = form.save(commit=False)

        category_name, obj.title, tags = self.__split(form.cleaned_data['title'])
        obj.category = self.__get_category(category_name)

        success_url = super(SetTagsAndCategorizeMixin, self).form_valid(form)

        # save tags
        if hasattr(self, 'object') and self.object:
            self.__create_tags(self.object, tags)

        return success_url


class IsOwnerMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self._object = self.get_object()
            if self._object.owner.id != request.user.id:
                messages.warning(request, "You are not allowed to edit this article")
                return redirect('articles:detail', self._object.id)

        return super(IsOwnerMixin, self).dispatch(request, *args, **kwargs)


class ArticleListMixin(object):
    def get_queryset(self):
        return super(ArticleListMixin, self).get_queryset() \
            .order_by('-modified').select_related('owner__profile', 'category') \
            .prefetch_related(Prefetch("tag_set", to_attr="tags"))


class ArticleListView(ArticleListMixin, ArticleSearchMixin,
                      CategorySearchMixin, TagSearchMixin,
                      LoginRequiredMixin, CategoryListViewMixin, ListView):
    model = Article
    template_name = 'article_list.jinja2'
    paginate_by = 10


class OwnersArticleListView(ArticleListMixin, LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article_list.jinja2'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super(OwnersArticleListView, self).get_context_data(**kwargs)
        context_data['owner'] = User.objects.get(pk=self.kwargs['owner_id']).username
        return context_data


class ArticleDetailAndCreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'article_detail.jinja2'

    def get_success_url(self):
        return reverse('articles:detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.article = Article.objects.get(pk=self.kwargs['pk'])
        return super(ArticleDetailAndCreateCommentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super(ArticleDetailAndCreateCommentView, self).get_context_data(**kwargs)
        article = Article.objects.get(pk=self.kwargs['pk'])
        context_data['article'] = article
        context_data['tags'] = Tag.objects.filter(article=article)
        context_data['category'] = \
            article.category.name if article.category.name != categories.NOT_CATEGORISED else ''
        context_data['comments'] = Comment.objects.filter(article=self.kwargs['pk']).select_related('user', 'user__profile').order_by('modified')
        return context_data


class ArticleEditMixin(object):

    model = Article
    template_name = 'article_form.jinja2'
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context_data = super(ArticleEditMixin, self).get_context_data(**kwargs)
        context_data['DEMO'] = settings.DEMO
        return context_data

    def get_form(self, form_class=None):
        form = super(ArticleEditMixin, self).get_form()
        template_choices = [('', 'テンプレート')]
        template_articles = Article.objects.filter(category__name__startswith='/template/')

        template_choices += \
            [(x.id, rebuild_edit_title_without_template_prefix(x)) for x in template_articles]

        form.fields['templates'].choices = template_choices
        return form


class ArticleCreateView(LoginRequiredMixin, ArticleEditMixin, SetTagsAndCategorizeMixin, CreateView):

    def get_success_url(self):
        return reverse('articles:detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, ArticleEditMixin, SetTagsAndCategorizeMixin,
                        IsOwnerMixin, UpdateView):

    def get_success_url(self):
        if self._object:
            return reverse('articles:detail', kwargs={'pk': self._object.id})
        else:
            return reverse('articles:list')

    def get_object(self, **kwargs):

        # 既に生成済みの場合は，そのオブジェクトを返却する(dispatchでも呼び出すため複数回呼ばれる）
        if not hasattr(self, '_object'):
            self._object = super(ArticleUpdateView, self).get_object(**kwargs)

        return self._object

    def get_initial(self):
        data = super(ArticleUpdateView, self).get_initial()
        article = self.get_object()
        data['title'] = rebuild_edit_title(article)

        return data


class ArticleDeleteView(IsOwnerMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles:list')
    template_name = "article_confirm_delete.jinja2"


@require_POST
def delete_comment(request, article_id):
    comment_id = request.POST.get('comment_id')
    if comment_id:
        obj = Comment.objects.get(pk=comment_id)
        if obj.user == request.user or request.user.is_superuser:
            obj.delete()
        else:
            messages.warning(
                request, "You are not allowed to edit this comment")

    return redirect('articles:detail', article_id)


@require_GET
def select_template(request):
    article_id = request.GET.get('article')

    article = get_object_or_404(Article, pk=article_id)
    title = rebuild_edit_title_without_template_prefix(article)

    result = {}
    result['title'] = template_formatting(request, title)
    result['body'] = template_formatting(request, article.body)
    return JsonResponse(result)
