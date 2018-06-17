from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item import Item
from shiftcontent import exceptions as x
from datetime import datetime


@attr('item')
class EventTest(BaseTestCase):

    def test_instantiating_event(self):
        """ Instantiating item """
        item = Item()
        self.assertIsInstance(item, Item)

    def test_printable_repr(self):
        """ Getting printable representation of an item """
        item = Item()
        repr = item.__repr__()
        self.assertIn('<ContentItem', repr)

    def test_event_gets_creation_date_upon_instantiation(self):
        """ Event gets creation date upon instantiating """
        item = Item()
        self.assertIsInstance(item.props['created'], datetime)

    def test_property_access(self):
        """ Can use property access for getting item props"""
        item = Item()
        self.assertIsInstance(item.created, datetime)

    def test_property_access_set(self):
        """ Property access for setting item props"""
        dt = 'datetime!'
        item = Item()
        item.created = dt
        self.assertEquals(dt, item.props['created'])
        item.props = 'something'
        self.assertEquals('something', item.props)

    def test_can_check_for_attribute_presence(self):
        """ Can use hasattr to check for prop existence"""
        item = Item()
        self.assertFalse(hasattr(item, 'whatever'))

    def test_populate_event_from_dict(self):
        """ Can populate event from dict """
        data = dict(
            path="123/456",
            author='1',
            object_id=123,
            data={'what': 'some payload'}
        )

        item = Item(**data)
        for prop in data.keys():
            self.assertEquals(data[prop], getattr(item, prop))

    def test_getting_item_as_dict(self):
        """ Getting event as dict """
        item = Item(data=dict(prop='value'))
        self.assertTrue(type(item.to_dict()) is dict)
        self.assertTrue(type(item.to_dict()['data']) is dict)

    def test_get_db_representation(self):
        """ Getting db representation of an item """
        item = Item(data=dict(prop='value'))
        result = item.to_db()
        self.assertTrue(type(result['data']) is str)

    def test_raise_when_setting_non_dictionary_data(self):
        """ Raise when setting a payload that is not a dict """
        item = Item()
        with self.assertRaises(x.ContentItemError) as cm:
            item.data = [123]

        self.assertIn('Data must be a dictionary', str(cm.exception))

    def test_raise_when_fails_to_decode_data_string(self):
        """ Raise when data string can not be decoded """
        item = Item()
        with self.assertRaises(x.ContentItemError) as cm:
            item.data = 'no-a-json-string'
        self.assertIn('Failed to decode data string', str(cm.exception))

    def test_getting_item_data(self):
        """ Getting event payload """
        data = dict(some='payload_goes_here')
        item = Item(data=data)
        self.assertTrue(type(item.data) is dict)