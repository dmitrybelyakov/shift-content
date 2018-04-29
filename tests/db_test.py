import unittest
from nose.plugins.attrib import attr

import os
import shutil
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


from shiftcontent import Db
from shiftcontent import exceptions as x
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import MetaData

@attr('db')
class DbTest(unittest.TestCase):

    @property
    def tmp(self):
        """ Get path to temp data """
        tmp = os.path.join(
            os.getcwd(), 'var', 'data', 'tests', 'tmp'
        )
        if not os.path.exists(tmp):
            os.makedirs(tmp, exist_ok=True)
        return tmp

    @property
    def db_url(self):
        """ Get test db url """
        url = 'sqlite:///{}/test.db'.format(self.tmp)
        return url

    def tearDown(self):
        """ Cleanup """
        super().tearDown()
        tests = os.path.join(os.getcwd(), 'var', 'data', 'tests')
        if os.path.exists(tests): shutil.rmtree(tests)

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
        mock_engine = 'I am an engine'
        db = Db(engine=mock_engine)
        self.assertEquals(mock_engine, db.engine)

    def test_use_custom_meta(self):
        """ Use custom metadata object """
        mock_meta = 'I am metadata!'
        db = Db(self.db_url, meta=mock_meta)
        self.assertEquals(mock_meta, db.meta)

    def test_create_fresh_metadata(self):
        """ Creating metadata object on first access """
        db = Db(self.db_url)
        meta = db.meta
        self.assertIsInstance(meta, MetaData)

    def test_creating_tables(self):
        """ Creating tables"""
        db_url = self.db_url
        db = Db(db_url)
        employees = Table('employees', db.meta,
            Column('id', Integer, primary_key=True),
            Column('name', String(128)),
            Column('full_name', String(128)),
        )

        addresses = Table('addresses', db.meta,
            Column('id', Integer, primary_key=True),
            Column('user_id', None, ForeignKey('employees.id')),
            Column('email_address', String(256), nullable=False)
        )

        db.meta.create_all()
        self.assertIn(employees, db.meta.sorted_tables)
        self.assertIn(addresses, db.meta.sorted_tables)







