from categories import NOT_CATEGORISED
from categories.models import Category


class CategoryException(Exception):
    pass


def validation_name(name):
    if not name:
        raise CategoryException('カテゴリ名を入力してください')
    if name.find('/') >= 0:
        raise CategoryException('カテゴリ名に「/」は使用できません')
    if name == NOT_CATEGORISED[:-1]:
        raise CategoryException('この名称はカテゴリ名に使用できません')

    return True


def validation_unique_path(path):
    if Category.objects.filter(name__startswith=path):
        raise CategoryException('同じ名前のカテゴリが存在します')
    return True
