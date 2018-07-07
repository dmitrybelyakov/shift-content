from shiftevent_tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftevent.event import Event
from shiftevent.handlers import Dummy2


@attr('event', 'handler', 'dummy2')
class Dummy1Test(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating dummy2 handler """
        handler = Dummy2(self.db)
        self.assertIsInstance(handler, Dummy2)

    def test_handle_event(self):
        """ Handler Dummy2 handles event"""
        handler = Dummy2(self.db)
        event = Event(
            type='DUMMY_EVENT',
            payload={'prop': 'val'}
        )

        event = handler.handle(event)
        self.assertIn('dummy_handler2', event.payload)

    def test_rollback_event(self):
        """ Handler Dummy2 rolling back an event """
        handler = Dummy2(self.db)
        event = Event(
            type='DUMMY_EVENT',
            payload={'prop': 'val'}
        )

        event = handler.handle(event)
        self.assertIn('dummy_handler2', event.payload)

        handler.rollback(event)
        self.assertNotIn('dummy_handler2', event.payload)
