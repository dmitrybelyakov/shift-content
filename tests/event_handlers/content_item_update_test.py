from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemUpdate
from shiftcontent.item import Item
from shiftcontent import db


@attr('event', 'handler', 'content_item_update')
class ContentItemUpdateTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item create handler """
        handler = ContentItemUpdate(db=self.db)
        self.assertIsInstance(handler, ContentItemUpdate)

    def test_handle_event(self):
        """ Handler content item update handles event"""

        items = db.tables['items']

        author = 123
        object_id = str(uuid1())

        item = Item('plain_text', **dict(
            author=author,
            object_id=object_id,
            body='Initial body'
        ))

        # remember old data
        old_data = item.to_dict(serialized=True)

        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        item.body = 'Updated body'
        new_data = item.to_dict(serialized=True)

        # update now
        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=author,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        )

        handler = ContentItemUpdate(db=self.db)
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item(**record)
            self.assertEquals('Updated body', updated.body)

    def test_rollback_event(self):
        """ Handler content item update rolling back changes """
        items = db.tables['items']

        author = 123
        object_id = str(uuid1())

        item = Item('plain_text', **dict(
            author=author,
            object_id=object_id,
            body='Initial body'
        ))

        # remember old data
        old_data = item.to_dict(serialized=True)

        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        item.body = 'Updated body'
        new_data = item.to_dict(serialized=True)

        # update now
        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE',
            author=author,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        )

        handler = ContentItemUpdate(db=self.db)
        handler.handle(event)

        # now rollback
        handler.rollback(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            rolled_back = Item(**record)
            self.assertEquals('Initial body', rolled_back.body)


