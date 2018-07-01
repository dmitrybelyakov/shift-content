from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from shiftcontent.events.event import Event
from shiftcontent.events.handlers import ContentItemCreate


@attr('event', 'handler', 'content_item_create')
class Dummy1Test(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item create handler """
        handler = ContentItemCreate(db=self.db)
        self.assertIsInstance(handler, ContentItemCreate)

    def test_handle_event(self):
        """ Handler content item create handles event"""
        handler = ContentItemCreate(db=self.db)
        object_id = str(uuid1())
        event = Event(
            id=123,
            type='CONTENT_ITEM_CREATE',
            author=123,
            object_id=object_id,
            payload=dict(
                type='plain_text',
                data=dict(body='I am the body field')
            )
        )

        handler.handle(event)
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query)
            self.assertIsNotNone(result.fetchone())

    # def test_rollback_event(self):
    #     """ Handler content iten create rolling back an event """
    #     handler = Dummy1(self.db)
    #     event = Event(
    #         type='DUMMY_EVENT',
    #         payload={'prop': 'val'}
    #     )
    #
    #     event = handler.handle(event)
    #     self.assertIn('dummy_handler1', event.payload)
    #
    #     handler.rollback(event)
    #     self.assertNotIn('dummy_handler1', event.payload)
