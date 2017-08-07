from datetime import date
import categories
from .models import Tag


def template_formatting(request, template_val):
    today = date.today()
    return template_val.replace('%year', today.strftime('%Y')) \
        .replace('%month', today.strftime('%m')) \
        .replace('%day', today.strftime('%d')) \
        .replace('%name', request.user.username)


def rebuild_edit_title(article):
    tags = [x.name for x in Tag.objects.filter(article=article)]
    return __rebuild_edit_title(article.title, article.category.name, tags)


def rebuild_edit_title_without_template_prefix(article):
    title = article.title
    tags = [x.name for x in Tag.objects.filter(article=article)]
    category = article.category.name
    if category.startswith('/template/'):
        category = category[category.find('/', 1):]

    return __rebuild_edit_title(title, category, tags)


def __rebuild_edit_title(title, category, tags=None):
    result = ''
    if not category or \
                    category in ('/', categories.NOT_CATEGORISED):

        result = title
    else:
        result = category + title

    if not tags:
        return result

    tags_str = ', '.join(tags)
    if tags_str:
        result = result + ' #' + tags_str

    return result
