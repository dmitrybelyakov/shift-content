from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from pprint import pprint as pp
import random


# def build_tree(item, children):
#
#     ids = list(child['id'] for child in children)
#     ids.append(item['id'])
#
#     # wrap nodes
#     item = dict(node=item, children=[])
#     children = [dict(node=c, children=[]) for c in children if all(
#         i in ids for i in c['path'].split('.')  # filter orphans
#     )]
#
#     iteration = 0
#     def add_to_tree(item, tree):
#         nonlocal iteration
#         iteration += 1
#         print('ITERATION:' + str(iteration))
#         is_child = tree['node']['id'] == item['node']['path'].split('.')[-1]
#         if is_child:
#             tree['children'].append(item)
#             del children[children.index(item)]
#         else:
#             tree['children'] = [add_to_tree(item, c) for c in tree['children']]
#
#         return tree
#
#     while children:
#         for child in children:
#             add_to_tree(child, item)
#
#     return item



def build_tree(item, children):

    ids = list(child['id'] for child in children)
    ids.append(item['id'])

    # filter orphans
    children = [c for c in children if all(
        i in ids for i in c['path'].split('.')
    )]

    def in_tree(id, tree):
        if tree['id'] == id:
            return True
        return any(in_tree(id, child) for child in tree['children'])

    it = 0
    def add_to_tree(item, tree):
        if in_tree(item['id'], tree):
            return tree

        parent_ids = item['path'].split('.')
        parents = []
        for parent_id in parent_ids:
            p = [c for c in children if c['id'] == parent_id]
            if p:
                parents.append(p[0])

        for parent in parents:
            if not in_tree(parent['id'], tree):
                tree = add_to_tree(parent, tree)

        is_child = tree['id'] == item['path'].split('.')[-1]
        if is_child:
            tree['children'].append(item)
        else:
            tree['children'] = [add_to_tree(item, c) for c in tree['children']]

        return tree



    for child in children:
        item = add_to_tree(child, item)


    return item





@attr('tree')
class TreeTest(BaseTestCase):

    def test_build_tree_from_materialised_path(self):
        """ Building tree from materialised path """
        root = dict(name='Root', id='11', path='', children=[])
        children = [
            dict(name='Parent 1', id='9', path='11', children=[]),
            dict(name='Child 1', id='1', path='11.9', children=[]),
            dict(name='Child 2', id='2', path='11.9.1', children=[]),
            dict(name='Child 3', id='3', path='11.9.1.2', children=[]),
            dict(name='Child 4', id='4', path='11.9.1.2.3', children=[]),

            dict(name='Parent 2', id='10', path='11', children=[]),
            dict(name='Child 5', id='5', path='11.10', children=[]),
            dict(name='Child 6', id='6', path='11.10.5', children=[]),
            dict(name='Child 7', id='7', path='11.10.5.6', children=[]),
            dict(name='Child 8', id='8', path='11.10.5.6.7', children=[]),

            dict(name='An orphan', id='12', path='11.20.26.99', children=[]),
        ]

        random.shuffle(children)
        children = sorted(children, key=lambda c: len(c['path'].split('.')), reverse=True)
        tree = build_tree(root, children)

        for c in children:
            print(c['name'], c['path'])

        # print('-'*80)
        # print('GOT TREE:')
        pp(tree)
        # print('-'*80)



        

