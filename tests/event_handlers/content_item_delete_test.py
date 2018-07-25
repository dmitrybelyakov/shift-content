from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemDelete
from shiftcontent.item import Item


@attr('event', 'handler', 'content_item_delete')
class ContentItemDeleteTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item create handler """
        handler = ContentItemDelete(db=self.db)
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

        handler = ContentItemDelete(db=self.db)
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNone(result)

    def test_rollback_event(self):
        """ Handler content item delete rolling back changes """
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

        rollback = item.to_dict()
        rollback['meta']['created'] = rollback['meta']['created'].strftime(
            item.date_format
        )

        event = Event(
            id=123,
            type='CONTENT_ITEM_DELETE',
            author=456,
            object_id=object_id,
            payload=None,
            payload_rollback=rollback
        )

        handler = ContentItemDelete(db=self.db)
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
