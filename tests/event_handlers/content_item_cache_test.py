from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftcontent import db
from shiftcontent.event_handlers import ContentItemCache


@attr('event', 'handler', 'content_cache_cache')
class ContentItemCacheTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item cache handler """
        handler = ContentItemCache(db=self.db)
        self.assertIsInstance(handler, ContentItemCache)

    def test_handle_event(self):
        """ Handler content item cache handles event"""
        cache_service.init()

        # create item
        object_id = str(uuid1())
        item = Item(
            type='plain_text',
            author=123,
            object_id=object_id,
            body='Some body content'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # trigger event
        handler = ContentItemCache(db=self.db)
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_INDEX',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=None
        ))

        # assert cached
        cached = cache_service.get(object_id)
        self.assertEquals(item.object_id, cached.object_id)
        self.assertEquals(item.body, cached.body)

        # cleanup
        cache_service.delete_all()
        cache_service.disconnect()

    def test_rollback_event(self):
        """ Handler content item cache rolling back changes """
        cache_service.init()

        # create item
        object_id = str(uuid1())
        item = Item(
            type='plain_text',
            author=123,
            object_id=object_id,
            body='Some body content'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # trigger event
        handler = ContentItemCache(db=self.db)
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_INDEX',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=None
        ))

        # assert cached
        cached = cache_service.get(object_id)
        self.assertEquals(item.object_id, cached.object_id)
        self.assertEquals(item.body, cached.body)

        # cleanup
        cache_service.delete_all()
        cache_service.disconnect()
