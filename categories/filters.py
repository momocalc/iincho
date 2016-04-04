from .models import Category
import urllib.parse


class Node():
    def __init__(self, parent_path, name):
        self.is_route = False
        self.children = []
        self.name = name
        self.count = 0
        self.sort_number = 0
        self.path = ""

        if parent_path:
            self.path = parent_path + name + '/'
        elif name:
            self.path = '/' + name + '/'


    def __getattr__(self, item):
        if item == 'encoded_path':
            return urllib.parse.quote(self.path)

        if item == 'sorted_children':
            return sorted(self.children, key=lambda x:(x.sort_number, x.name))

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


def __is_final_part(splitted_category_name, current_idx):
    """
    splitされたカテゴリ名の指定インデックスがカテゴリ名の最終要素であるか
    最終要素が空要素ならば，そのひとつ前を最終要素とする
    :param splitted_category_name: カテゴリを/で区切ったリスト
    :param current_idx: 確認対象Index
    :return: splitted_category_name[current_idx]がカテゴリ名の最終要素であるかどうか
    """
    if current_idx == len(splitted_category_name) - 1:
        return True

    if current_idx  == len(splitted_category_name) - 2:
        if not splitted_category_name[-1]:
            return True

    return False


def __make_tree(parent, category, splitted_category_name,  current_idx):
    if not splitted_category_name:
        return

    if current_idx >= len(splitted_category_name):
        return

    if splitted_category_name[current_idx] == '':
        __make_tree(parent, category, splitted_category_name, current_idx + 1)
        return

    current_name = splitted_category_name[current_idx]

    # 親をさがす
    tmp_list = [x for x in parent.children if x.name == current_name]

    if tmp_list:
        tmp_node = tmp_list[0]
    else:
        tmp_node = Node(parent.path, current_name)
        parent.children.append(tmp_node)
        if __is_final_part(splitted_category_name, current_idx):
            tmp_node.sort_number = category.sort_number

    tmp_node.count += category.num_articles
    __make_tree(tmp_node, category, splitted_category_name, current_idx + 1)


def category_tree(categories):
    tree = Node('', '')
    for category in categories:
        __make_tree(tree, category, category.name.split('/'), 0)
    return tree
