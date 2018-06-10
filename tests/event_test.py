from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.event import Event
from shiftcontent import exceptions as x
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
        self.assertIn('<Event', repr)

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

    def test_can_check_for_attribute_presence(self):
        """ REGRESSION: can use hasattr to check for prop existence"""
        event = Event()
        self.assertFalse(hasattr(event, 'whatever'))

    def test_populate_event_from_dict(self):
        """ Can populate event from dict """
        data = dict(
            type="TEST",
            author='1',
            object_id=123,
            payload={'what': 'some payload'}
        )

        event = Event(**data)
        for prop in data.keys():
            self.assertEquals(data[prop], getattr(event, prop))

    def test_raise_when_modifying_event_id_directly(self):
        """ Raize exception when modifying event id"""
        event = Event()
        with self.assertRaises(x.EventError):
            event.id = '123'

    def test_getting_event_as_dict(self):
        """ Getting event as dict """
        event = Event()
        self.assertTrue(type(event.to_dict()) is dict)

    def test_raise_when_setting_non_dictionary_payload(self):
        """ Raise when setting a payload that is not a dict """
        event = Event()
        with self.assertRaises(x.EventError):
            event.payload = 'crap'

    def test_setting_payload(self):
        """ Setting event payload """
        data = dict(some='payload_goes_here')
        event = Event(payload=data)
        self.assertTrue(type(event.props['payload']) is str)

    def test_getting_event_payload(self):
        """ Getting event payload """
        data = dict(some='payload_goes_here')
        event = Event(payload=data)
        self.assertTrue(type(event.payload) is dict)

