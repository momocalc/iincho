from typing import Optional, List

from .models import Category
import urllib.parse


class Node(object):
    """
    category tree node
    """

    def __init__(self, name, parent=None):
        self.is_route = False
        self.children = []
        self.name = name
        self.count = 0
        self.sort_number = 0
        self.parent = parent

    def __getattr__(self, item):
        if item == 'encoded_path':
            return urllib.parse.quote(self.path)

        if item == 'sorted_children':
            return sorted(self.children, key=lambda x: (x.sort_number, x.name))

        if item == 'path':
            if self.parent:
                return self.parent.path + self.name + '/'
            elif self.name:
                return self.name + '/'
            else:
                return ''

    def __str__(self):
        if not self.children:
            return ""

        res = ""
        for child in self.children:
            res += child.name + ':[ ' + str(child) + ' ], '

        return res


def split_nodes(full_cate_name: str) -> List[Node]:
    """
    カテゴリ名からノードリストを作成
    :param full_cate_name: カテゴリ名(ex: foo/var/hoge/)
    :return: ルートからのノードのリスト
    """
    result = []
    p = None
    for level in full_cate_name.split('/'):
        if level:
            n = Node(level, parent=p)
            result.append(n)
            p = n

    return result


def __get_level_name(level: int, full_cate_name: str) -> Optional[str]:
    s = full_cate_name.split('/')
    if level >= len(s):
        return None
    if not s[level]:
        return None
    return s[level]


def __is_leaf(level: int, name: str) -> bool:
    return level == name.count('/') - 1


def __make_tree(parent: Node, category: Category, level: int):
    cat_name = __get_level_name(level, category.name)
    if not cat_name:
        return

    # すでに登録済みかチェック
    tmp_list = [x for x in parent.children if x.name == cat_name]
    if tmp_list:
        node = tmp_list[0]
    else:
        node = Node(cat_name, parent=parent)
        parent.children.append(node)
        if __is_leaf(level, category.name):
            node.sort_number = category.sort_number

    node.count += category.num_articles
    __make_tree(node, category, level + 1)


def category_tree(categories: List[Category]) -> List[Node]:
    """
    カテゴリのリストをノードリスト(木構造)に変換する
    :param categories:
    :return:
    """
    root = Node('')
    for category in categories:
        __make_tree(root, category, 0)
    return root
