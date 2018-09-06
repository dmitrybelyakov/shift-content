from tests.base import BaseTestCase
from nose.plugins.attrib import attr


@attr('trees')
class UtilsTest(BaseTestCase):

    def test_trees_test(self):
        """ Testing tree sorting """
        tree = [
            '1/2/',
            '2/2/',
            '3/2/',
            '4/2/',
            '5/2/',
            '6/2/',
            '7/2/',
            '8/2/',
            '9/2/',
            '10/2/',
            '11/2/',
            # '1/2/3/4/5',
            # '1/2',
            # '1/10/6/22',
            # '1/10/60/22',
            # '1/100/60/22',
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
