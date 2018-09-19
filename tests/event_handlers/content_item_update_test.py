from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemUpdate
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import cache_service
from shiftcontent import search_service
import json


@attr('event', 'handler', 'content_item_update')
class ContentItemUpdateTest(BaseTestCase):

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
        """ Instantiating content item update handler """
        handler = ContentItemUpdate()
        self.assertIsInstance(handler, ContentItemUpdate)

    def test_handle_event(self):
        """ Handler content item update handles event"""
        author = 123
        object_id = str(uuid1())

        item = Item(
            id=123,
            type='plain_text',
            author=author,
            object_id=object_id,
            body='Initial body'
        )

        # remember old data
        old_data = item.to_json()

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        item.body = 'Updated body'
        new_data = item.to_json()

        # update now
        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=author,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        )

        handler = ContentItemUpdate()
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item()
            updated.from_db(record)
            self.assertEquals('Updated body', updated.body)

    def test_update_item_updates_cache(self):
        """ Update item handler updates cache """
        object_id = str(uuid1())
        type = 'plain_text'

        # create item
        item = Item(
            id=123,
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )

        old_data = item.to_json()

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in cache
        self.assertIsNone(cache_service.get(object_id))

        updated = 'Updated body'
        item.body = updated
        new_data = item.to_json()

        # now update
        handler = ContentItemUpdate()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=123,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        ))

        # assert in cache
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cached)
        self.assertEquals(updated, cached.body)

    def test_update_item_updates_index(self):
        """ Update item handler updates index """
        object_id = str(uuid1())
        type = 'plain_text'

        # create item
        item = Item(
            id=123,
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )

        old_data = item.to_json()

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in index
        self.assertIsNone(search_service.get(type, object_id))

        updated = 'Updated body'
        item.body = updated
        new_data = item.to_json()

        # now update
        handler = ContentItemUpdate()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=123,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        ))

        # assert in index
        found = search_service.get(type, object_id)
        self.assertIsNotNone(found)
        self.assertEquals(updated, found['_source']['body'])

    def test_rollback_event(self):
        """ Handler content item update rolling back changes """
        author = 123
        object_id = str(uuid1())

        item = Item(
            id=123,
            type='plain_text',
            author=author,
            object_id=object_id,
            body='Initial body'
        )

        # remember old data
        old_data = item.to_json()

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        item.body = 'Updated body'
        new_data = item.to_json()

        # update now
        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=author,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        )

        handler = ContentItemUpdate()
        handler.handle(event)

        # now rollback
        handler.rollback(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            rolled_back = Item()
            rolled_back.from_db(record)
            self.assertEquals('Initial body', rolled_back.body)

    def test_update_item_rollback_updates_cache(self):
        """ Update item rollback updates cache """
        object_id = str(uuid1())
        type = 'plain_text'

        # create
        item = Item(
            id=123,
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # remember old data
        initial_body = item.body
        old_data = item.to_json()

        # update now
        item.body = 'Updated body'
        new_data = item.to_json()

        # drop cache
        cache_service.delete(object_id)
        self.assertIsNone(cache_service.get(object_id))

        # rollback
        handler = ContentItemUpdate()
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=123,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        ))

        # assert in cache
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cached)
        self.assertEquals(initial_body, cached.body)

    def test_update_item_rollback_updates_index(self):
        """ Update item rol updates index """
        object_id = str(uuid1())
        type = 'plain_text'

        # create
        item = Item(
            id=123,
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # remember old data
        initial_body = item.body
        old_data = item.to_json()

        # update now
        item.body = 'Updated body'
        new_data = item.to_json()

        # drop from index
        search_service.delete(type, object_id)
        self.assertIsNone(search_service.get(type, object_id))

        # rollback
        handler = ContentItemUpdate()
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=123,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        ))

        # assert in cache
        found = search_service.get(type, object_id)
        self.assertIsNotNone(found)
        self.assertEquals(initial_body, found['_source']['body'])

