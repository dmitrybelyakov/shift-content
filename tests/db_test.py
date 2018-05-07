from tests.base import BaseTestCase
from nose.plugins.attrib import attr


import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


from shiftcontent import Db
from shiftcontent import Event
from shiftcontent import exceptions as x
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import MetaData


@attr('db')
class DbTest(BaseTestCase):

    def tables(self, meta):
        """ Creates test table definitions """
        tables = dict()
        tables['employees'] = Table('employees', meta,
            Column('id', Integer, primary_key=True),
            Column('name', String(128)),
            Column('full_name', String(128)),
        )

        tables['addresses'] = Table('addresses', meta,
            Column('id', Integer, primary_key=True),
            Column('user_id', None, ForeignKey('employees.id')),
            Column('email_address', String(256),nullable=False)
        )

        return tables

    # --------------------------------------------------------------------------

    def test_instantiate_db(self):
        """ Instantiating database """
        db = Db('sqlite:///:memory:', echo=True)
        self.assertIsInstance(db, Db)

    def test_raise_when_no_engine_or_url(self):
        """ Raise exception when neither db_url nor engine were passsed"""
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

    def test_append_event(self):
        """ Appending an event """
        data = dict(
            type="TEST",
            author='1',
            object_id=123,
            payload='some payload'
        )
        event = Event(**data)
        self.db.append_event(event)
        self.assertEquals(1, event.id)



    def test_creating_tables(self):
        """ Creating tables"""
        db_url = self.db_url
        db = Db(db_url)
        tables = self.tables(db.meta)
        db.meta.create_all()
        self.assertIn(tables['employees'], db.meta.sorted_tables)
        self.assertIn(tables['addresses'], db.meta.sorted_tables)

    def test_can_insert(self):
        """ Inserting database records"""
        db = Db(self.db_url)
        tables = self.tables(db.meta)
        db.meta.create_all()

        employees = tables['employees']
        insert = employees.insert().values(name='Test')

        conn = db.engine.connect()
        result = conn.execute(insert)
        id = result.inserted_primary_key
        self.assertEquals([1], id)

    def test_shorthand_insert(self):
        """ Insert using shorthand"""
        db = Db(self.db_url)
        tables = self.tables(db.meta)
        db.meta.create_all()

        employees = tables['employees']
        conn = db.engine.connect()
        result = conn.execute(employees.insert(), name="DEMO")
        self.assertIn(1, result.inserted_primary_key)






