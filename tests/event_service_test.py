from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import EventService
from shiftcontent import Event


@attr('event', 'service')
class EventServiceTest(BaseTestCase):

    def test_create_event_service(self):
        """ Creating event service"""
        service = EventService(db=self.db)
        self.assertIsInstance(service, EventService)

    def test_raise_validation_errors_when_creating_invalid_event(self):
        """ Raise validation exception when creating event from bad data"""
        service = EventService(db=self.db)
        try:
            service.event(
                type='DUMMY_EVENT',
                object_id=None,
                author=456,
                payload={'what': 'IS THIS'}
            )
        except x.InvalidEvent as err:
            self.assertIn('object_id', err.validation_errors)

    def test_create_event(self):
        """ Creating an event """
        service = EventService(db=self.db)
        event = service.event(
            type='DUMMY_EVENT',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'},
        )
        self.assertEquals(1, event.id)

    def test_raise_on_missing_handler_when_creating_an_event(self):
        """ Raise exception on missing event handler when creating an event"""
        service = EventService(db=self.db)
        with self.assertRaises(x.EventError):
            service.event(
                type='UNKNOWN_EVENT_TYPE',
                object_id=123,
                author=456,
                payload={'wtf': 'IS THIS'}
            )

    def test_get_event_by_id(self):
        """ Getting event by id"""
        service = EventService(db=self.db)
        event = service.event(
            type='DUMMY_EVENT',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'},
        )

        id = event.id
        event = service.get_event(id)
        self.assertIsInstance(event, Event)
        self.assertEquals(id, event.id)

    def test_fail_to_emit_unsaved_event(self):
        """ Error out on emitting unsaved event """
        service = EventService(db=self.db)
        event = Event()
        with self.assertRaises(x.EventError):
            service.emit(event)

    def test_raise_on_missing_handler_when_emitting_an_event(self):
        """ Raise exception on missing event handler when emitting an event"""
        service = EventService(db=self.db)
        event = Event(
            type='UNKNOWN_EVENT_TYPE',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'}
        )
        with self.assertRaises(x.EventError):
            service.emit(event)

    def test_can_emit_an_event_and_run_handler_sequence(self):
        """ Emitting an event and running handler sequence"""
        service = EventService(db=self.db)
        event = service.event(
            type='DUMMY_EVENT',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'}
        )

        processed = service.emit(event)
        self.assertIn('dummy_handler1', processed.payload)
        self.assertIn('dummy_handler2', processed.payload)











