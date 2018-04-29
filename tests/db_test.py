import unittest
from nose.plugins.attrib import attr

import os
import shutil
from shiftcontent.db import Db
from shiftcontent import exceptions as x
from sqlalchemy.engine.base import Engine

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

    def db_url(self):
        """ Get test db url """
        url = 'sqlite://{}/test.db'.format(self.tmp)
        return url

    def tearDown(self):
        """ Cleanup """
        super().tearDown()
        tests = os.path.join(os.getcwd(), 'var', 'data', 'tests')
        if os.path.exists(tests):
            shutil.rmtree(tests)

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
