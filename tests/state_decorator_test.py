import unittest
from nose.plugins.attrib import attr


@attr('stateful')
class StateDecorators(unittest.TestCase):

    def test_define_tables_with_meta(self):
        """ Defining tables with metadata object """
        def once():
            from shiftcontent.services import content
            return content

        def twice():
            from shiftcontent.services import content
            return content

        self.assertTrue(once() is twice())
