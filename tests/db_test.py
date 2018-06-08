from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import MetaData

from shiftcontent import Db
from shiftcontent.event import Event
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

    # -------------------------------------------------------------------------
    # db operations
    # -------------------------------------------------------------------------

    def test_append_events(self):
        """ Appending events """
        self.db.echo = True

        event = Event(
            type="TEST",
            author='1',
            object_id=123,
            payload={'dict': 'some payload'}
        )
        self.db.append_event(event)

        event2 = Event(
            type="TEST",
            author='1',
            object_id=123,
            payload={'dict': 'more payload'}
        )
        self.db.append_event(event2)

        self.assertEquals(1, event.id)
        self.assertEquals(2, event2.id)

    # def test_get_projection(self):
    #     """ Getting a projection """
    #
    #     event1 = Event(
    #         type='TEST',
    #         author='1',
    #         object_id=123,
    #         payload={
    #             'field1': 'somevalue 1',
    #             'field2': None,
    #             'field4': 'initial value'
    #         }
    #     )
    #
    #     event2 = Event(
    #         type='TEST',
    #         author='1',
    #         object_id=123,
    #         payload={
    #             'field1': 'somevalue 2',
    #             'field2': 'Updating field 2',
    #             'field4': 'initial value updated'
    #         }
    #     )
    #
    #     event3 = Event(
    #         type='TEST',
    #         author='1',
    #         object_id=123,
    #         payload={
    #             'field1': 'somevalue 3',
    #             'field3': 'Created field 3',
    #             'field4': None
    #         }
    #     )
    #
    #     self.db.append_event(event1)
    #     self.db.append_event(event2)
    #     self.db.append_event(event3)
    #
    #     projection = self.db.get_projection(123)
    #     self.assertEquals('somevalue 3', projection['field1'])
    #     self.assertEquals('Updating field 2', projection['field2'])
    #     self.assertEquals('Created field 3', projection['field3'])
    #     self.assertEquals(None, projection['field4'])






