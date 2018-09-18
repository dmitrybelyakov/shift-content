from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
import time
from shiftevent.event import Event
from shiftcontent.item import Item
from shiftcontent import search_service
from shiftcontent import db
from shiftcontent.event_handlers import ContentItemRemoveFromIndex


@attr('event', 'handler', 'content_item_remove_from_index')
class ContentItemRemoveFromIndexTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item removefrom index handler """
        handler = ContentItemRemoveFromIndex()
        self.assertIsInstance(handler, ContentItemRemoveFromIndex)

    def test_handle_event(self):
        """ Handler content item remove from index handles event"""
        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        handler = ContentItemRemoveFromIndex()
        object_id = str(uuid1())

        # index first
        item = Item(
            id=123,
            type='plain_text',
            author=123,
            object_id=object_id,
            body='Some body content'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert indexed
        search_service.put_to_index(item)
        time.sleep(1)
        self.assertIsNotNone(search_service.get(item.type, object_id))

        # now trigger event
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_REMOVE_FROM_INDEX',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=item.to_json()
        ))

        # assert not in index
        time.sleep(1)
        self.assertIsNone(search_service.get(item.type, object_id))

        # cleanup
        search_service.drop_index(item.type)
        search_service.disconnect()

    def test_rollback_event(self):
        """ Handler content item remove from index rolling back changes """

        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        handler = ContentItemRemoveFromIndex()
        object_id = str(uuid1())

        # prepare data for rollback
        item = Item(
            id=123,
            type='plain_text',
            author=123,
            object_id=object_id,
            body='Some body content'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in index
        self.assertIsNone(search_service.get(item.type, object_id))

        # now rollback delete event
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_REMOVE_FROM_INDEX',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=item.to_json()
        ))

        # assert not in index
        time.sleep(1)
        self.assertIsNotNone(search_service.get(item.type, object_id))

        # cleanup
        search_service.drop_index(item.type)
        search_service.disconnect()
