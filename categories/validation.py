from categories import NOT_CATEGORISED
from categories.models import Category


def validation_name(name):
    if not name:
        raise AttributeError('カテゴリ名を入力してください')
    if name.find('/') >= 0:
        raise AttributeError('カテゴリ名に「/」は使用できません')
    if name == NOT_CATEGORISED[:-1]:
        raise AttributeError('この名称はカテゴリ名に使用できません')

    return True


def validation_unique_path(path):
    if Category.objects.filter(name__startswith=path):
        raise AttributeError('同じ名前のカテゴリが存在します')
    return True
