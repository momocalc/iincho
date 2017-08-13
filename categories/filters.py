from typing import Optional

from .models import Category
import urllib.parse


class Node(object):
    """
    category tree node
    """

    def __init__(self, parent_path, name):
        self.is_route = False
        self.children = []
        self.name = name
        self.count = 0
        self.sort_number = 0
        self.path = ""

        if parent_path:
            self.path = parent_path + '/' + name
        elif name:
            self.path = name

    def __getattr__(self, item):
        if item == 'encoded_path':
            return urllib.parse.quote(self.path)

        if item == 'sorted_children':
            return sorted(self.children, key=lambda x: (x.sort_number, x.name))

    def __str__(self):
        if not self.children:
            return ""

        res = ""
        for child in self.children:
            res += child.name + ':[ ' + str(child) + ' ], '

        return res


def split_path(category):
    result = []
    p = None
    for level in category.split('/'):
        if level:
            n = Node(p, level)
            result.append(n)
            p = n.path

    return result


def __get_level_name(level: int, name: str) -> Optional[str]:
    s = name.split('/')
    if level >= len(s):
        return None
    if not s[level]:
        return None
    return s[level]


def __is_leaf(level: int, name: str) -> bool:
    return level == name.count('/')


def __make_tree(parent, category, level):
    cat_name = __get_level_name(level, category.name)
    if not cat_name:
        return

    # すでに登録済みかチェック
    tmp_list = [x for x in parent.children if x.name == cat_name]
    if tmp_list:
        node = tmp_list[0]
    else:
        node = Node(parent.path, cat_name)
        parent.children.append(node)
        if __is_leaf(level, cat_name):
            node.sort_number = category.sort_number

    node.count += category.num_articles
    __make_tree(node, category, level + 1)


def category_tree(categories):
    root = Node('', '')
    for category in categories:
        __make_tree(root, category, 0)
    return root
