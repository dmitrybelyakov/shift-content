from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemDelete
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftcontent import search_service


@attr('event', 'handler', 'content_item_delete')
class ContentItemDeleteTest(BaseTestCase):

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
        """ Instantiating content item delete handler """
        handler = ContentItemDelete()
        self.assertIsInstance(handler, ContentItemDelete)

    def test_handle_event(self):
        """ Handler content item delete handles event"""
        object_id = str(uuid1())
        item = Item(
            type='plain_text',
            object_id=object_id,
            author=456,
            body='I have a body'
        )

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        event = Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None
        )

        handler = ContentItemDelete()
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNone(result)

    def test_delete_item_removes_it_from_cache(self):
        """ Delete item handler removes item from cache """
        object_id = str(uuid1())
        type = 'plain_text'

        # create
        item = Item(
            type=type,
            object_id=object_id,
            author=456,
            body='I have a body'
        )

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.set_field('id', result.inserted_primary_key[0], initial=True)

        # cache
        cache_service.set(item)
        self.assertIsNotNone(cache_service.get(object_id))

        # now delete
        handler = ContentItemDelete()
        handler.handle( Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None
        ))

        # assert no longer in cache
        self.assertIsNone(cache_service.get(object_id))

    def test_delete_item_removes_it_from_index(self):
        """ Delete item handler removes item from index """
        object_id = str(uuid1())
        type = 'plain_text'

        # create
        item = Item(
            type=type,
            object_id=object_id,
            author=456,
            body='I have a body'
        )

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.set_field('id', result.inserted_primary_key[0], initial=True)

        # index
        search_service.put_to_index(item)
        self.assertIsNotNone(search_service.get(type, object_id))

        # now delete
        handler = ContentItemDelete()
        handler.handle( Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None
        ))

        # assert no longer in index
        self.assertIsNone(search_service.get(type, object_id))

    def test_rollback_event(self):
        """ Handler content item delete rolling back changes """
        object_id = str(uuid1())
        item = Item(
            id=123,
            type='plain_text',
            object_id=object_id,
            author=456,
            body='I have a body'
        )

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        rollback = item.to_json()

        event = Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None,
            payload_rollback=rollback
        )

        handler = ContentItemDelete()
        handler.handle(event)
        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNone(result)

        # now rollback
        handler.rollback(event)

        # assert recovered
        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            recovered = conn.execute(query).fetchone()
            self.assertIsNotNone(recovered)

    def test_delete_item_rollback_caches_item(self):
        """ Delete item rollback caches item """
        object_id = str(uuid1())
        type = 'plain_text'

        # create
        item = Item(
            type=type,
            object_id=object_id,
            author=456,
            body='I have a body'
        )

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.set_field('id', result.inserted_primary_key[0], initial=True)

        # cache
        cache_service.set(item)
        self.assertIsNotNone(cache_service.get(object_id))

        event = Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None,
            payload_rollback=item.to_json()
        )

        # delete
        handler = ContentItemDelete()
        handler.handle(event)
        self.assertIsNone(cache_service.get(object_id))

        # rollback
        handler.rollback(event)

        # assert back in cache
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cached)
        self.assertEquals(item.body, cached.body)


    def test_delete_item_rollback_indexes_item(self):
        """ Delete item rollback put item to index """
        object_id = str(uuid1())
        type = 'plain_text'

        # create
        item = Item(
            type=type,
            object_id=object_id,
            author=456,
            body='I have a body'
        )

        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.set_field('id', result.inserted_primary_key[0], initial=True)

        # index
        search_service.put_to_index(item)
        self.assertIsNotNone(search_service.get(type, object_id))

        event = Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None,
            payload_rollback=item.to_json()
        )

        # delete
        handler = ContentItemDelete()
        handler.handle(event)
        self.assertIsNone(search_service.get(type, object_id))

        # rollback
        handler.rollback(event)

        # assert back in index
        found = search_service.get(type, object_id)
        self.assertIsNotNone(found)
        self.assertEquals(item.body, found['_source']['body'])
