from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import EventService
from shiftcontent import Event


@attr('event', 'service')
class EventServiceTest(BaseTestCase):

    def test_create_content_service(self):
        """ Creating content service"""
        service = EventService(db=self.db)
        self.assertIsInstance(service, EventService)

    def test_raise_validation_errors_when_creating_invalid_event(self):
        """ Raise validation exception when creating event from bad data"""
        service = EventService(db=self.db)
        try:
            service.event(
                type='SOME_EVENT_TYPE',
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
            type='SOME_EVENT_TYPE',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'}
        )
        self.assertEquals(1, event.id)

    def test_fail_to_emit_unsaved_event(self):
        """ Error out on emitting unsaved event """
        service = EventService(db=self.db)
        event = Event()
        with self.assertRaises(x.EventError):
            service.emit(event)


