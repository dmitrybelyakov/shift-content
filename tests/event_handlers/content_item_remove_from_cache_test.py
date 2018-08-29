from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
import time
from shiftevent.event import Event
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftcontent.event_handlers import ContentItemRemoveFromCache


@attr('event', 'handler', 'content_item_remove_from_cache')
class ContentItemRemoveFromCacheTest(BaseTestCase):

    def setUp(self):
        cache_service.init()
        super().setUp()

    def tearDown(self):
        cache_service.delete_all()
        cache_service.disconnect()
        super().tearDown()

    # --------------------------------------------------------------------------
    # tests
    # --------------------------------------------------------------------------

    def test_instantiating_handler(self):
        """ Instantiating content item removefrom index handler """
        handler = ContentItemRemoveFromCache(db=self.db)
        self.assertIsInstance(handler, ContentItemRemoveFromCache)

    def test_handle_event(self):
        """ Handler content item remove from cache handles event"""
        # cache first
        object_id = str(uuid1())
        item = Item(
            id=123,
            type='plain_text',
            author=123,
            object_id=object_id,
            body='Some body content'
        )
        cache_service.set(item)

        # now trigger delete event
        handler = ContentItemRemoveFromCache(db=self.db)
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_REMOVE_FROM_CACHE',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=item.to_json()
        ))

        # assert removed from cache
        cached = cache_service.get(object_id)
        self.assertIsNone(cached)

    def test_rollback_event(self):
        """ Handler content item remove from cache rolling back changes """
        # prepare data for rollback
        object_id = str(uuid1())
        item = Item(
            id=123,
            type='plain_text',
            author=123,
            object_id=object_id,
            body='Some body content'
        )

        # assert not in cached
        self.assertIsNone(cache_service.get(object_id))

        # now rollback delete event
        handler = ContentItemRemoveFromCache(db=self.db)
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_REMOVE_FROM_CACHE',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=item.to_json()
        ))

        # assert cached after rollback
        self.assertIsNotNone(cache_service.get(object_id))
