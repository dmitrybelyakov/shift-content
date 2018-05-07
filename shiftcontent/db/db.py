from sqlalchemy import create_engine

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime


from shiftcontent.db.tables import define_tables
from shiftcontent import exceptions as x


class Db:
    db_url = None
    db_params = None
    tables = dict()
    _meta = None
    _engine = None

    def __init__(self, db_url=None, engine=None, meta=None, **db_params):
        """
        Instantiates database object
        Accepts database URL to connect the engine to and a dict of db engine
        params that will be passed to te engine. See sqlalchmy engine docs for
        possible params: http://docs.sqlalchemy.org/en/latest/core/engines.html

        Alternatively can accept a ready-made engine via engine parameter which
        is useful for integration into applications when we don't need to
        manage separate connection pools.

        Additionally accepts a custom metadata object. Pass this if you want
        to integration content tables in already existing metadata catalogue
        of your application.

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
        self._meta = meta
        self.tables = define_tables(self.meta)

    @property
    def engine(self):
        """
        Core interface to the database. Maintains connection pool.
        :return: sqlalchemy.engine.base.Engine
        """
        if not self._engine:
            self._engine = create_engine(self.db_url, **self.db_params)
        return self._engine

    # todo: always close the result or connection
    # todo: want transactions? use engine.begin() context manager

    @property
    def meta(self):
        """
        Metadata
        A catalogue of tables and columns.
        :return: sqlalchemy.sql.schema.MetaData
        """
        if not self._meta:
            self._meta = MetaData(self.engine)
        return self._meta

    def append_event(self, event):
        """
        Append event
        :param event: shiftcontent.events.Event
        :return: shiftcontent.events.Event
        """
        if event.id:
            msg = 'Appending events with existing ids is not allowed. '
            x.EventLogError(msg)

        events = self.tables['events']
        with self.engine.begin() as conn:
            result = conn.execute(events.insert(), **event.to_dict())
            event.id = result.inserted_primary_key[0]

        return event












