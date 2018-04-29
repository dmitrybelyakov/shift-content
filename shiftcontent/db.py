from sqlalchemy import create_engine

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

# todo: with core we don't get cascades
from shiftcontent import exceptions as x


class Db:
    db_url = None
    db_params = None
    _engine = None

    def __init__(self, db_url=None, engine=None, **db_params):
        """
        Instantiates database object
        Accepts database URL to connect the engine to and a dict of db engine
        params that will be passed to te engine. See sqlalchmy engine docs for
        possible params: http://docs.sqlalchemy.org/en/latest/core/engines.html

        Alternatively can accept a ready-made engine via engine parameter which
        is useful for integration into applications when we don't need to
        manage separate connection pools.

        :param db_url: str, database url
        :param engine: sqalchemy engine
        :param echo: bool, whether to print queries to console
        """
        if not db_url and not engine:
            msg = 'Can\'t instantiate database:db_url or engine required'
            raise x.DatabaseError(msg)

        self.db_url = db_url
        self.db_params = db_params
        self._engine = engine

    @property
    def engine(self):
        """
        Get engine
        Instantiates database engine from configuration
        :return: sqlalchemy.engine.base.Engine
        """

        if self._engine:
            return self._engine

        self._engine = create_engine(self.db_url, **self.db_params)
        return self._engine







