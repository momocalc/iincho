from .models import Category
import urllib.parse


class Node():
    def __init__(self, parent_path, name):
        self.is_route = False
        self.children = []
        self.name = name
        self.count = 0

        self.path = ""

        if parent_path:
            self.path = parent_path + name + '/'
        elif name:
            self.path = '/' + name + '/'

    def set_route(self, current_node):
        if current_node.startswith(self.path):
            self.is_route = True

    def __getattr__(self, item):
        if item == 'encoded_path':
            return urllib.parse.quote(self.path)

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


def make_tree(parent, vals, num_articles, current_idx):
    if not vals:
        return

    if current_idx >= len(vals):
        return

    if vals[current_idx] == '':
        make_tree(parent, vals, num_articles, current_idx+1)
        return

    current_name = vals[current_idx]

    tmp_list = [x for x in parent.children if x.name == current_name]

    if tmp_list:
        tmp_node = tmp_list[0]
    else:
        tmp_node = Node(parent.path, current_name)
        parent.children.append(tmp_node)

    tmp_node.count += num_articles
    make_tree(tmp_node, vals, num_articles, current_idx+1)


def category_tree(categories):
    tree = Node('', '')
    for category in categories:
        make_tree(tree, category.name.split('/'), category.num_articles, 0)
    return tree
