from shiftcontent_tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent import define_tables
from sqlalchemy import MetaData


@attr('db', 'tables')
class TablesTest(BaseTestCase):

    def test_define_tables_with_meta(self):
        """ Defining tables with metadata object """
        meta = MetaData()
        tables = define_tables(meta)
        for table in tables.values():
            self.assertEquals(meta, table.metadata)






