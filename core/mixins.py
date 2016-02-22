import re


class PopQueryHelper(object):

    def pop_queries(self, *keys):
        if hasattr(self, 'query'):
            q = self.query
        else:
            q = self.request.GET.get('query')
        if not q:
            return None

        pattern = r'(^|[\s]+)({0})(\S+)'.format('|'.join(keys))
        self.query = re.sub(pattern, r'\1', q)
        return [x[2] for x in re.findall(pattern, q)]


class TagSearchMixin(PopQueryHelper, object):

    def get_queryset(self):
        queryset = super(TagSearchMixin, self).get_queryset()

        tags = self.pop_queries('#')
        if not tags:
            return queryset

        in_q = ','.join(['%s'] * len(tags))
        sql = 'articles_article.id in (select article_id from articles_tag where name in ({0}) ' \
            'group by article_id having count(*) = %s)'.format(in_q)

        params = tags
        params.append(len(tags))  # count
        return queryset.extra(where=[sql], params=params)


class CategorySearchMixin(PopQueryHelper, object):

    def get_queryset(self):
        queryset = super(CategorySearchMixin, self).get_queryset()

        categories = self.pop_queries('c:')
        if not categories:
            return queryset

        for c in categories:
            queryset = queryset.filter(category__name__contains=c)

        return queryset
