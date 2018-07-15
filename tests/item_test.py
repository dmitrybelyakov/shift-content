from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item import Item
from shiftcontent import exceptions as x
from datetime import datetime
from pprint import pprint as pp



@attr('item')
class ItemTest(BaseTestCase):

    def test_instantiating_event(self):
        """ Instantiating item """
        item = Item(fields=['body'])
        self.assertIsInstance(item, Item)

    def test_printable_repr(self):
        """ Getting printable representation of an item """
        item = Item(fields=['body'])
        repr = item.__repr__()
        self.assertIn('<ContentItem', repr)

    def test_event_gets_creation_date_upon_instantiation(self):
        """ Event gets creation date upon instantiating """
        item = Item(fields=['body'])
        self.assertIsInstance(item.props['created'], datetime)

    def test_property_access(self):
        """ Can use property access for getting item props"""
        item = Item(fields=['body'])
        self.assertIsInstance(item.created, datetime)

    def test_property_access_set(self):
        """ Property access for setting item props"""
        dt = 'datetime!'
        item = Item(fields=['body'])
        item.created = dt
        self.assertEquals(dt, item.props['created'])
        item.props = 'something'
        self.assertEquals('something', item.props)

    def test_can_check_for_attribute_presence(self):
        """ Can use hasattr to check for prop existence"""
        item = Item(fields=['body'])
        self.assertFalse(hasattr(item, 'whatever'))

    def test_populate_event_from_dict(self):
        """ Can populate event from dict """
        data = dict(
            path="123/456",
            author='1',
            object_id=123,
            data={'body': 'some payload'}
        )

        item = Item(fields=['body'], **data)
        for prop in data.keys():
            self.assertEquals(data[prop], getattr(item, prop))

    def test_fail_to_set_nonexistent_data_field(self):
        """ Data fields that weren't initialized can't be set """
        item = Item(fields=['a_field'])
        item.not_initialized = 'some value'
        self.assertNotIn('not_initialized', item.data.keys())

    def test_fail_to_set_nonexistent_field_when_bulk_setting_data(self):
        """ Setting data skips uninitialized fields """
        data = dict(a_field='some_value', undefined='some other vaue')
        item = Item(fields=['a_field'])
        item.set_data(data)
        self.assertIn('a_field', item.data.keys())
        self.assertEquals(data['a_field'], item.a_field)
        self.assertNotIn('undefined', item.data.keys())

    def test_getting_item_as_dict(self):
        """ Getting event as dict """
        item = Item(fields=['body'], data=dict(prop='value'))
        self.assertTrue(type(item.to_dict()) is dict)
        self.assertTrue(type(item.to_dict()['data']) is dict)

    def test_get_db_representation(self):
        """ Getting db representation of an item """
        item = Item(fields=['body'], data=dict(body='value'))
        result = item.to_db()
        self.assertTrue(type(result['data']) is str)

    def test_raise_when_setting_non_dictionary_data(self):
        """ Raise when setting a payload that is not a dict """
        item = Item(fields=['body'])
        with self.assertRaises(x.ContentItemError) as cm:
            item.data = [123]

        self.assertIn('Data must be a dictionary', str(cm.exception))

    def test_raise_when_fails_to_decode_data_string(self):
        """ Raise when data string can not be decoded """
        item = Item(fields=['body'])
        with self.assertRaises(x.ContentItemError) as cm:
            item.data = 'no-a-json-string'
        self.assertIn('Failed to decode data string', str(cm.exception))

    def test_getting_item_data(self):
        """ Getting event payload """
        data = dict(body='payload_goes_here')
        item = Item(fields=['body'], data=data)
        self.assertTrue(type(item.data) is dict)

    def test_getting_data_field(self):
        """ Getting data fields directly  """
        data = dict(
            id=1234,
            type='markdown',
            author='1234',
            object_id='12345-67890',
            data=dict(
                title='I am a content item',
                body='I have some body text'
            )
        )

        item = Item(fields=['title', 'body'], **data)
        self.assertEquals(data['data']['title'], item.title)
        self.assertEquals(data['data']['body'], item.body)

    def test_setting_data_field(self):
        """ Setting data fields """
        item = Item(fields=['a_field'])
        item.a_field = 'some value'
        self.assertEquals('some value', item.data['a_field'])
        self.assertEquals('some value', item.a_field)

