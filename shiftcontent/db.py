from sqlalchemy import create_engine

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

class Db:
    engine = None
    meta = None

    def __init__(self):
        """
        Instantiate database object
        """
        self.get_engine()
        self.get_meta()

    def get_meta(self):
        """
        Access metadata object.
        :return: sqlalchemy.sql.schema.MetaData
        """
        if not self.meta:
            self.meta = MetaData()
        return self.meta

    def get_engine(self, echo=False):
        """
        Get engine
        Instantiates database engine from configuration
        :param echo: bool, log sql queries
        :return: sqlalchemy.engine.base.Engine
        """

        if self.engine:
            return self.engine

        url = 'mysql://{user}:{password}@{host}:{port}/{db}'
        # url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
        url += '?charset=utf8'
        url = url.format(
            user='root',
            password='god',
            host='127.0.0.1',
            port='3306',
            db='shiftcontent',
        )

        self.engine = create_engine(url, echo=echo)
        return self.engine





