from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import EventService
from shiftcontent import Event


@attr('event', 'handlers')
class EventHandlersTest(BaseTestCase):

    def test_emitting_an_event(self):
        """ Emitting an event """
        service = EventService(db=self.db)
        event = service.event(
            type='DUMMY_EVENT',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'}
        )

        result = service.emit(event)
        self.assertEquals(event, result)
