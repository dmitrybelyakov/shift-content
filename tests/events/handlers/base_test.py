from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.events.handlers import Dummy1
from shiftcontent.events.handlers import NoType
from shiftcontent.events.event import Event
from shiftcontent import exceptions as x


@attr('event', 'handler', 'base')
class BaseHandlerTest(BaseTestCase):
    """
    Base event handler test. Since it's abstract we're gonna test it through
    a concrete implementations.
    """
    def test_handlers_have_access_to_db(self):
        """ Handlers have access to database"""
        handler = Dummy1(db=self.db)
        self.assertEquals(self.db, handler.db)

    def test_handler_must_define_event_type(self):
        """ Handlers must define event type """
        with self.assertRaises(x.MissingEventType) as cm:
            NoType(db=self.db)
        self.assertIn('Event type undefined for handler', str(cm.exception))

    def test_raise_error_on_handling_unsupported_event(self):
        """ Raise error on handling unsupported events """
        event = Event(type='UNSUPPORTED')
        handler = Dummy1(db=self.db)
        with self.assertRaises(x.UnsupportedEventType) as cm:
            handler.handle_event(event)
        self.assertIn('can\'t support events of this type', str(cm.exception))

    def test_raise_error_on_rolling_back_usupported_event(self):
        """ Raise error when rolling back unsupported event """
        event = Event(type='UNSUPPORTED')
        handler = Dummy1(db=self.db)
        with self.assertRaises(x.UnsupportedEventType) as cm:
            handler.rollback_event(event)
        self.assertIn('can\'t support events of this type', str(cm.exception))
