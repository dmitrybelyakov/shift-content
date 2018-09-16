from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemCreate


@attr('event', 'handler', 'content_item_create')
class ContentItemCreateTest(BaseTestCase):

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

