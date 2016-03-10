from datetime import date
import categories
def template_formatting(request, template_val):
    today = date.today()
    return template_val.replace('%year', today.strftime('%Y')) \
        .replace('%month',  today.strftime('%m')) \
        .replace('%day', today.strftime('%d')) \
        .replace('%name', request.user.username)


def rebuild_edit_title(title,category,tags):
    result = ''
    if category == categories.NOT_CATEGORISED:
        result = title
    else:
        result = category + title

    tags = ', '.join(tags)
    if tags:
        result = title + ' #' + tags

    return result
