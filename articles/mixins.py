import re

from django.contrib import messages
from django.db.models import Q, Prefetch
from django.shortcuts import redirect

import categories
from categories.models import Category
from .models import Tag


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

    def __split_category(self, title):
        text = re.sub(r'/*\s*/\s*', '/', title.strip())
        last_slash = text.rfind('/')

        if last_slash < 1:
            category = categories.NOT_CATEGORISED
        else:
            category = text[:last_slash]
            if category.startswith('/'):
                category = category[1:]

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
