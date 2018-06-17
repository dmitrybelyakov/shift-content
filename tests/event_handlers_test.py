from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import EventService
from shiftcontent import Event
from uuid import uuid1


@attr('event', 'handlers')
class EventHandlersTest(BaseTestCase):

    def test_emit_dummy_event(self):
        """ Emitting a dummy event """
        service = EventService(db=self.db)
        event = service.event(
            type='DUMMY_EVENT',
            object_id=123,
            author=456,
            payload={'wtf': 'IS THIS'}
        )

        result = service.emit(event)
        self.assertEquals(event, result)

    @attr('zzz')
    def test_emit_content_ite_create(self):
        """ Emitting content item creation event """
        service = EventService(db=self.db)
        event = service.event(
            type='CONTENT_ITEM_CREATE',
            author='123',
            object_id=uuid1(),
            payload=dict(
                body='This is the content of this item\'s body'
            )
        )

        service.emit(event)

        print(event)
