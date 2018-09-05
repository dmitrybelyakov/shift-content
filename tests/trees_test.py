from tests.base import BaseTestCase
from nose.plugins.attrib import attr
import shiftschema
import shiftschema.schema
from shiftschema.schema import Schema
from pprint import pprint as pp
from shiftcontent.utils import import_by_name


@attr('trees')
class UtilsTest(BaseTestCase):

    def test_trees_test(self):
        """ Testing tree sorting """
        tree = [
            '1/2/3/4/5',
            '1/2',
            '1/10/6/22',
            '1/10/60/22',
            '1/100/60/22',
        ]

        tree2 = [
            '001/002/003/004/005',
            '001/002',
            '001/010/06/022',
            '001/010/060/022',
            '001/100/060/022',
        ]

        # for i in sorted(tree):
        #     print(i)
        #
        # for i in sorted(tree2):
        #     print(i)
