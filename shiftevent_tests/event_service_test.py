from shiftevent_tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftevent import exceptions as x
from shiftevent.event_service import EventService
from shiftevent.event import Event
from shiftevent.handlers import Dummy1


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
            payload={'what': 'IS THIS'},
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
                payload={'what': 'IS THIS'}
            )

    def test_get_event_by_id(self):
        """ Getting event by id"""
        service = EventService(db=self.db)
        event = service.event(
            type='DUMMY_EVENT',
            object_id=123,
            author=456,
            payload={'what': 'IS THIS'},
        )

        id = event.id
        event = service.get_event(id)
        self.assertIsInstance(event, Event)
        self.assertEquals(id, event.id)

    def test_instantiate_handler(self):
        """ Instantiating handler """
        handler_definitions = dict(DUMMY_EVENT=[Dummy1])
        service = EventService(db=self.db, handlers=handler_definitions)
        event = Event(type='DUMMY_EVENT', id=123, payload=dict(some='payload'))
        event = service.emit(event)
        self.assertIn('dummy_handler1', event.payload)

    def test_raise_when_handler_not_defined_as_a_class(self):
        """ Raise an error when handler is not a class """
        handler_definitions = dict(DUMMY_EVENT=[Dummy1(db=self.db)])
        service = EventService(db=self.db, handlers=handler_definitions)
        event = Event(type='DUMMY_EVENT', id=123, payload=dict(some='payload'))
        with self.assertRaises(x.HandlerInstantiationError) as cm:
            service.emit(event)
        self.assertIn('has to be a class, got', str(cm.exception))

    def test_raise_when_handler_doesnt_iherit_from_base(self):
        """ Raise error when handler does not extend from base """
        class Handler:
            def __init__(self, *args, **kwargs):
                pass

            def handle(self, *args, **kwargs):
                pass

        handler_definitions = dict(DUMMY_EVENT=[Handler])
        service = EventService(db=self.db, handlers=handler_definitions)
        event = Event(type='DUMMY_EVENT', id=123, payload=dict(some='payload'))
        with self.assertRaises(x.HandlerInstantiationError) as cm:
            service.emit(event)
        self.assertIn(
            'Handler implementations must extend BaseHandler',
            str(cm.exception)
        )

    def test_raise_on_missing_handler_when_emitting_an_event(self):
        """ Raise exception on missing event handler when emitting an event"""
        service = EventService(db=self.db)
        event = Event(
            type='UNKNOWN_EVENT_TYPE',
            object_id=123,
            author=456,
            payload={'what': 'IS THIS'}
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
            payload={'what': 'IS THIS'}
        )

        processed = service.emit(event)
        self.assertIn('dummy_handler1', processed.payload)
        self.assertIn('dummy_handler2', processed.payload)











