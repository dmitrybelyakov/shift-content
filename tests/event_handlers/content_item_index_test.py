from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
import time
from shiftevent.event import Event
from shiftcontent.item import Item
from shiftcontent import search_service
from shiftcontent import db
from shiftcontent.event_handlers import ContentItemIndex


@attr('event', 'handler', 'content_item_index')
class ContentItemIndexTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item index handler """
        handler = ContentItemIndex(db=self.db)
        self.assertIsInstance(handler, ContentItemIndex)

    def test_handle_event(self):
        """ Handler content item index handles event"""

        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        handler = ContentItemIndex(db=self.db)
        object_id = str(uuid1())

        # create first
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

        # now trigger indexing event
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_INDEX',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=None
        ))

        time.sleep(1)

        found = search_service.get(object_id)
        self.assertIsNotNone(found)
        self.assertEquals(object_id, found['_source']['object_id'])

        # cleanup
        search_service.drop_index()
        search_service.disconnect()

    def test_rollback_event(self):
        """ Handler content item index rolling back changes """

        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        handler = ContentItemIndex(db=self.db)
        object_id = str(uuid1())

        # create first
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

        # now trigger indexing event
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_INDEX',
            author=123,
            object_id=object_id,
            payload=None,
            payload_rollback=None
        ))

        time.sleep(1)

        found = search_service.get(object_id)
        self.assertIsNotNone(found)
        self.assertEquals(object_id, found['_source']['object_id'])

        # cleanup
        search_service.drop_index()
        search_service.disconnect()
