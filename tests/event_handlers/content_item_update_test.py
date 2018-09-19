from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemUpdate
from shiftcontent.item import Item
from shiftcontent import db
import json


@attr('event', 'handler', 'content_item_update')
class ContentItemUpdateTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item update handler """
        handler = ContentItemUpdate()
        self.assertIsInstance(handler, ContentItemUpdate)

    def test_handle_event(self):
        """ Handler content item update handles event"""

        items = db.tables['items']

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

    def update_item_updates_cache(self):
        """ Update item handler updates cache """
        self.fail('Implement me!')

    def update_item_updates_index(self):
        """ Update item handler updates index """
        self.fail('Implement me!')

    def test_rollback_event(self):
        """ Handler content item update rolling back changes """
        items = db.tables['items']

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

    def update_item_rollback_updates_cache(self):
        """ Update item rollback updates cache """
        self.fail('Implement me!')

    def update_item_rollback_updates_index(self):
        """ Update item rol updates index """
        self.fail('Implement me!')

