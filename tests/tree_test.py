from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from pprint import pprint as pp
import random


def build_tree(item, children):
    print('BUILDING TREE NOW')
    pp(item)
    pp(children)




@attr('tree')
class TreeTest(BaseTestCase):

    def test_build_tree_from_materialised_path(self):
        """ Building tree from materialised path """
        root = dict(name='Root', id='11', path='')
        children = [
            dict(name='Parent 1', id='9', path='11'),
            dict(name='Child 1', id='1', path='11.9'),
            dict(name='Child 2', id='2', path='11.9.1'),
            dict(name='Child 3', id='3', path='11.9.1.2'),
            dict(name='Child 4', id='4', path='11.9.1.2.3'),

            dict(name='Parent 2', id='10', path='11'),
            dict(name='Child 5', id='5', path='11.10'),
            dict(name='Child 6', id='6', path='11.10.5'),
            dict(name='Child 7', id='7', path='11.10.5.6'),
            dict(name='Child 8', id='8', path='11.10.5.6.7'),

            dict(name='An orphan', id='12', path='11.20.26.99'),
        ]

        random.shuffle(children)
        build_tree(root, children)


        

