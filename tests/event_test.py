from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.events import Event
from datetime import datetime


@attr('event')
class EventTest(BaseTestCase):

    def test_instantiating_event(self):
        """ Instantiating event """
        event = Event()
        self.assertIsInstance(event, Event)

    def test_printable_repr(self):
        """ Getting printable representation of an event """
        event = Event()
        repr = event.__repr__()
        self.assertIn('<ContentEvent', repr)

    def test_event_gets_creation_date_upon_instantiation(self):
        """ Event gets creation date upon instantiating """
        event = Event()
        self.assertIsInstance(event.props['created'], datetime)

    def test_property_access(self):
        """ Can use property access for getting """
        event = Event()
        self.assertIsInstance(event.props['created'], datetime)

    def test_property_access_set(self):
        """ Property access for setting """
        dt = 'datetime!'
        event = Event()
        event.created = dt
        self.assertEquals(dt, event.props['created'])

        event.props = 'something'
        self.assertEquals('something', event.props)

    def test_populate_event_from_dict(self):
        """ Can populate event from dict """
        data = dict(
            id=123,
            type="TEST",
            author='1',
            object_id=123,
            payload='some payload'
        )

        event = Event(**data)
        for prop in data.keys():
            self.assertEquals(data[prop], getattr(event, prop))

    def test_getting_event_as_dict(self):
        """ Getting event as dict """
        event = Event()
        self.assertTrue(type(event.to_dict()) is dict)



