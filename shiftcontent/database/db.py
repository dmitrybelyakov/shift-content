from sqlalchemy import create_engine
from sqlalchemy import MetaData
from shiftcontent import exceptions as x
from shiftcontent.database.tables import define_tables


class Db:
    db_url = None
    db_params = None
    tables = dict()
    _meta = None
    _engine = None

    def __init__(self, *args, **kwargs):
        """
        Init database
        If any parameters are given to constructor, a delayed initializer is
        called withe these parameters.
        """
        if args or kwargs:
            self.init(*args, **kwargs)

    def init(
        self,
        db_url=None,
        engine=None,
        meta=None,
        dialect=None,
        **db_params
    ):
        """
        Delayed initializer
        Accepts database URL to connect to the engine  and a dict of db engine
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
        :param meta: metadata object to attach to
        :param dialect: str, only required for mysql
        :param db_params: dict, params to pass to engine
        """
        if not db_url and not engine:
            msg = 'Can\'t instantiate database:db_url or engine required'
            raise x.DatabaseError(msg)

        self.db_url = db_url
        self.db_params = db_params
        self._engine = engine
        self._meta = meta
        self.tables = define_tables(self.meta, dialect=dialect)

    @property
    def engine(self):
        """
        Core interface to the database. Maintains connection pool.
        :return: sqlalchemy.engine.base.Engine
        """
        if not self._engine:
            self._engine = create_engine(self.db_url, **self.db_params)
        return self._engine

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














