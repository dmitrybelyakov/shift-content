import unittest
from nose.plugins.attrib import attr

from shiftcontent.db import Db
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import MetaData
# from sqlalchemy import inspect
# from sqlalchemy import MetaData
# from sqlalchemy import Table, Column
# from sqlalchemy import Integer, String
# from sqlalchemy import ForeignKey


class DbTest(unittest.TestCase):

    def test_create_db(self):
        """ Creating an instance of our database class"""
        db = Db()
        self.assertIsInstance(db, Db)

    def test_create_sa_engine(self):
        """ Creating SA engine """
        db = Db()
        engine = db.get_engine()
        self.assertIsInstance(engine, Engine)

    def test_get_meta(self):
        """ Accessing metadata object"""
        db = Db()
        meta = db.get_meta()
        self.assertIsInstance(meta, MetaData)










    #
    # def test_work_with_metadata(self):
    #
    #     # describes the schema, is a collection of tables
    #     meta = MetaData()
    #
    #     user_table = Table('user', meta,
    #         Column('id', Integer, primary_key=True),
    #         Column('name', String(200)),
    #         Column('full_name', String(200))
    #     )
    #
    #     address_table = Table('address', meta,
    #         Column('id', Integer, primary_key=True),
    #         Column('email', String(100), nullable=False),
    #         Column('user_id', Integer, ForeignKey('user.id')),
    #     )
    #
    #     # this will create a table in the database if it does not exist
    #     # if table exists it will not be touched
    #     engine = self.get_engine()
    #     meta.create_all(engine)
    #
    # def test_using_reflection(self):
    #     meta = MetaData()
    #     engine = self.get_engine()
    #     user_table = Table('user', meta, autoload=True, autoload_with=engine)
    #     import pdb;
    #     pdb.set_trace()
    #     print(user_table)
    #
    # def test_using_inspector(self):
    #     engine = self.get_engine()
    #     inspector = inspect(engine)
    #     print(inspector)




