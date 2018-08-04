from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from sqlalchemy.dialects import mysql
from shiftcontent.database.tables import define_tables
from sqlalchemy import MetaData


@attr('db', 'tables')
class TablesTest(BaseTestCase):

    def test_define_tables_with_meta(self):
        """ Defining tables with metadata object """
        meta = MetaData()
        tables = define_tables(meta)
        for table in tables.values():
            self.assertEquals(meta, table.metadata)

    def test_switch_fileds_to_longtext_for_mysql(self):
        """ Fields column must be longtext for mysql """
        meta = MetaData()
        tables = define_tables(meta, dialect='mysql')
        items = tables['items']
        self.assertIsInstance(items.c.fields.type, mysql.LONGTEXT)






