import json
from collections import Mapping
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import sql
from sqlalchemy import desc, asc
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
        # todo: validate event with validator here

        if event.id:
            msg = 'Appending events with existing ids is not allowed. '
            x.EventLogError(msg)

        events = self.tables['events']
        with self.engine.begin() as conn:
            data = event.to_dict()
            del data['id']  # autoincremented
            result = conn.execute(events.insert(), **data)
            event.props['id'] = result.inserted_primary_key[0]

        return event

    # def merge_dicts(self, first, second):
    #     """
    #     Merge dicts
    #     Recursively merges two dictionaries
    #     :param first: dict, initial dict
    #     :param second: dict, overwritten wit hthe second
    #     :return: dict
    #     """
    #     for prop, val in second.items():
    #         first_dict = prop in first and isinstance(first[prop], dict)
    #         second_dict = prop in second and isinstance(second[prop], Mapping)
    #         if prop in first and first_dict and second_dict:
    #             self.merge_dicts(first[prop], second[prop])
    #         else:
    #             first[prop] = second[prop]
    #
    #     return first
    #
    # def get_projection(self, object_id):
    #     """
    #     Get projection
    #     Gets all the events for the given object id in chronological order
    #     and replays them recursively merging payload. Returns resulting
    #     payload.
    #
    #     :param object_id: str, object id to project
    #     :return:
    #     """
    #     events = self.tables['events']
    #     select = sql.select([events])\
    #         .where(events.c.object_id == object_id)\
    #         .order_by(asc('created'))
    #
    #     result = self.engine.execute(select)
    #     projection = dict()
    #     for row in result:
    #         payload = json.loads(row['payload'], encoding='utf-8')
    #         projection = self.merge_dicts(projection, payload)
    #     result.close()
    #
    #     return projection













