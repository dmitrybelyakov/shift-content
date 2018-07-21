from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import MetaData

from shiftcontent import Db
from shiftcontent import exceptions as x


@attr('db')
class DbTest(BaseTestCase):

    def test_instantiate_db(self):
        """ Instantiating database """
        db = Db('sqlite:///:memory:', echo=True)
        self.assertIsInstance(db, Db)

    def test_raise_when_no_engine_or_url(self):
        """ Raise exception when neither db_url nor engine were passed"""
        with self.assertRaises(x.DatabaseError):
            Db()

    def test_event_table_definitions_are_attached_to_meta(self):
        """ DB imports event table definition into content metadatata """
        db = Db('sqlite:///:memory:')
        self.assertIn('content_items', db.meta.tables)
        self.assertIn('event_store', db.meta.tables)

    def test_create_engine(self):
        """ Creating enginne on first access"""
        db = Db('sqlite:///:memory:', echo=True)
        engine = db.engine
        self.assertIsInstance(engine, Engine)

    def test_use_custom_engine(self):
        """ Skip engine creation when passed in """
        engine = create_engine(self.db_url)
        db = Db(engine=engine)
        self.assertEquals(engine, db.engine)

    def test_use_custom_meta(self):
        """ Use custom metadata object """
        meta = MetaData()
        db = Db(self.db_url, meta=meta)
        self.assertEquals(meta, db.meta)

    def test_create_fresh_metadata(self):
        """ Creating metadata object on first access """
        db = Db(self.db_url)
        meta = db.meta
        self.assertIsInstance(meta, MetaData)

    def test_define_tables_upon_db_creation(self):
        """ Load table definitions when instantiating db"""
        db = Db(self.db_url)
        for table in db.meta.sorted_tables:
            self.assertIn(table, db.tables.values())




