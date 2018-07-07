from shiftevent_tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftevent.event import Event
from shiftevent.handlers import Dummy1


@attr('event', 'handler', 'dummy1')
class Dummy1Test(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating dummy1 handler """
        handler = Dummy1(self.db)
        self.assertIsInstance(handler, Dummy1)

    def test_handle_event(self):
        """ Handler Dummy1 handles event"""
        handler = Dummy1(self.db)
        event = Event(
            type='DUMMY_EVENT',
            payload={'prop': 'val'}
        )

        event = handler.handle(event)
        self.assertIn('dummy_handler1', event.payload)

    def test_rollback_event(self):
        """ Handler Dummy1 rolling back an event """
        handler = Dummy1(self.db)
        event = Event(
            type='DUMMY_EVENT',
            payload={'prop': 'val'}
        )

        event = handler.handle(event)
        self.assertIn('dummy_handler1', event.payload)

        handler.rollback(event)
        self.assertNotIn('dummy_handler1', event.payload)
