from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemCreate
from shiftcontent import cache_service
from shiftcontent import search_service
from pprint import pprint as pp


@attr('event', 'handler', 'content_item_create')
class ContentItemCreateTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        cache_service.init()
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_prefix='content_tests'
        )

    def tearDown(self):
        """ Clean up """
        search_service.drop_all_indices()
        search_service.disconnect()
        cache_service.drop_cache(cache_service.cache_name)
        super().tearDown()

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_instantiating_handler(self):
        """ Instantiating content item create handler """
        handler = ContentItemCreate()
        self.assertIsInstance(handler, ContentItemCreate)

    def test_handle_event(self):
        """ Handler content item create handles event"""
        handler = ContentItemCreate()
        object_id = str(uuid1())
        event = Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type='plain_text',
                author=123,
                object_id=object_id,
                body='Some body content'
            )
        )

        handler.handle(event)
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNotNone(result)

    def test_created_item_is_cached(self):
        """ Create item handler caches item """
        type = 'plain_text'
        object_id = str(uuid1())

        # not in cache yet
        self.assertIsNone(cache_service.get(object_id))

        # create
        handler = ContentItemCreate()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type=type,
                author=123,
                object_id=object_id,
                body='Some body content'
            ))
        )

        # assert cached
        self.assertIsNotNone(cache_service.get(object_id))

    def test_created_item_is_put_to_index(self):
        """ Create item handler puts item to index """
        type = 'plain_text'
        object_id = str(uuid1())

        # not in index yet
        self.assertIsNone(search_service.get(type, object_id))

        # create
        handler = ContentItemCreate()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type=type,
                author=123,
                object_id=object_id,
                body='Some body content'
            ))
        )

        # assert indexed
        self.assertIsNotNone(search_service.get(type, object_id))

    def test_rollback_event(self):
        """ Handler content item create rolling back changes """
        handler = ContentItemCreate()
        object_id = str(uuid1())
        event = Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type='plain_text',
                author=123,
                object_id=object_id,
                body='Some body content'
            ),
            payload_rollback=None
        )

        # create
        handler.handle(event)

        # now roll back
        handler.rollback(event)

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNone(result)

    def test_create_item_rollback_removes_item_from_cache(self):
        """ Create item rollback removes item from cache """
        type = 'plain_text'
        object_id = str(uuid1())

        # create
        event = Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type=type,
                author=123,
                object_id=object_id,
                body='Some body content'
            ),
            payload_rollback=None
        )
        handler = ContentItemCreate()
        handler.handle(event)

        # assert in cache
        self.assertIsNotNone(cache_service.get(object_id))

        # now roll back
        handler.rollback(event)

        # assert not in cache
        self.assertIsNone(cache_service.get(object_id))

    def test_create_item_rollback_removes_item_from_index(self):
        """ Create item rollback removes item from index """
        type = 'plain_text'
        object_id = str(uuid1())

        # create
        event = Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type=type,
                author=123,
                object_id=object_id,
                body='Some body content'
            ),
            payload_rollback=None
        )
        handler = ContentItemCreate()
        handler.handle(event)

        # assert in index
        self.assertIsNotNone(search_service.get(type, object_id))

        # now roll back
        handler.rollback(event)

        # assert not in index
        self.assertIsNone(search_service.get(type, object_id))


