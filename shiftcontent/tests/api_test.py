import unittest
from nose.plugins.attrib import attr

from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String
from sqlalchemy import ForeignKey


class ApiTest(unittest.TestCase):
    def test_example(self):
        self.assertTrue(True)

    def get_engine(self):
        url = 'mysql://{user}:{password}@{host}:{port}/{db}'
        # url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
        url += '?charset=utf8'

        engine = create_engine(url.format(
            user='root',
            password='god',
            host='127.0.0.1',
            port='3306',
            db='shiftcontent',
        ))

        return engine

    def test_create_sa_engine(self):
        engine = self.get_engine()

        # connection will happen here
        res = engine.execute('select * from employee')
        row = res.fetchone()
        row2 = res.fetchone()
        print(row.emp_name)
        print(row2.emp_name)

    def test_work_with_metadata(self):

        # describes the schema, is a collection of tables
        meta = MetaData()

        user_table = Table('user', meta,
            Column('id', Integer, primary_key=True),
            Column('name', String(200)),
            Column('full_name', String(200))
        )

        address_table = Table('address', meta,
            Column('id', Integer, primary_key=True),
            Column('email', String(100), nullable=False),
            Column('user_id', Integer, ForeignKey('user.id')),
        )

        # this will create a table in the database if it does not exist
        # if table exists it will not be touched
        engine = self.get_engine()
        meta.create_all(engine)

    def test_using_reflection(self):
        meta = MetaData()
        engine = self.get_engine()
        user_table = Table('user', meta, autoload=True, autoload_with=engine)
        import pdb;
        pdb.set_trace()
        print(user_table)

    def test_using_inspector(self):
        engine = self.get_engine()
        inspector = inspect(engine)
        print(inspector)




