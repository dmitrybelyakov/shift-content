from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item import Item
from shiftcontent import exceptions as x
from datetime import datetime
import arrow
from pprint import pprint as pp


@attr('item')
class ItemTest(BaseTestCase):

    def test_instantiating_event(self):
        """ Instantiating item """
        item = Item(type='plain_text')
        self.assertIsInstance(item, Item)

    def test_initialize_item_fields_from_type(self):
        """ Initializing item fields from type upon creation """
        item = Item('plain_text')
        self.assertIn('body', item.fields)

    def test_raise_when_creating_item_of_undefined_type(self):
        """ Raise when creating item of undefined type """
        with self.assertRaises(x.ItemError) as cm:
            Item('lol')
        self.assertIn('is undefined', str(cm.exception))

    def test_printable_repr(self):
        """ Getting printable representation of an item """
        item = Item(type='plain_text')
        repr = item.__repr__()
        self.assertIn('<ContentItem', repr)

    def test_item_gets_creation_date_upon_instantiation(self):
        """ Item gets creation date upon instantiating """
        item = Item(type='plain_text')
        self.assertIsInstance(item.meta['created'], datetime)

    def test_property_access(self):
        """ Can use property access for getting item props"""
        item = Item(type='plain_text', body='copy')
        self.assertIsInstance(item.created, datetime)
        self.assertEquals('copy', item.body)

    def test_property_access_set(self):
        """ Property access for setting item props"""
        author = '123'
        item = Item(type='plain_text')
        item.author = author
        self.assertEquals(author, item.meta['author'])
        item.body = 'something'
        self.assertEquals('something', item.body)

    def test_can_check_for_attribute_presence(self):
        """ Can use hasattr to check for prop existence"""
        item = Item(type='plain_text')
        self.assertFalse(hasattr(item, 'whatever'))

    def test_populate_item_from_dict(self):
        """ Can populate item from dict """
        data = dict(
            path="123/456",
            author='1',
            object_id=123,
            fields={'body': 'some payload'}
        )

        # assert not class-level
        self.assertIsNone(Item.fields)
        self.assertIsNone(Item.meta)

        item = Item(type='plain_text', **data)
        for prop in data.keys():
            self.assertEquals(data[prop], getattr(item, prop))

    def test_fail_to_set_nonexistent_data_field(self):
        """ Data fields that weren't initialized can't be set """
        item = Item(type='plain_text')
        item.not_initialized = 'some value'
        self.assertNotIn('not_initialized', item.fields.keys())

    def test_check_field_for_being_updatable(self):
        """ testing field handles for being updatable """
        item = Item(type='plain_text')
        self.assertTrue(item.is_updatable('path'))
        self.assertTrue(item.is_updatable('body'))

        self.assertFalse(item.is_updatable('id'))
        self.assertFalse(item.is_updatable('object_id'))
        self.assertFalse(item.is_updatable('author_id'))
        self.assertFalse(item.is_updatable('nonexistent'))

    def test_fail_to_set_nonexistent_field_when_bulk_setting_data(self):
        """ Setting data skips uninitialized fields """
        fields = dict(body='some_value', undefined='some other value')
        item = Item(type='plain_text')
        item.set_fields(fields)
        self.assertIn('body', item.fields.keys())
        self.assertEquals(fields['body'], item.body)
        self.assertNotIn('undefined', item.fields.keys())

    def test_bulk_setting_meta_fields(self):
        """ Bulk-setting item meta fields from a dictionary """
        meta = dict(
            id=123,
            author=456,
            object_id='lksdjlkjdslkj-kjsdhkjshsdk',
            ignore_me='please'
        )

        item = Item(type='plain_text')
        item.meta = meta

        # assert not class-level
        self.assertIsNone(Item.meta)

        # but instance level
        self.assertEquals('plain_text', item.meta['type'])
        self.assertEquals(meta['id'], item.meta['id'])
        self.assertEquals(meta['author'], item.meta['author'])
        self.assertEquals(meta['object_id'], item.meta['object_id'])
        self.assertNotIn('ignore_me', item.meta)

    def test_getting_item_as_dict(self):
        """ Getting item as dict """
        item = Item(type='plain_text', data=dict(prop='value'))
        self.assertTrue(type(item.to_dict()) is dict)

    def test_getting_item_as_serialized_dict(self):
        """ Getting item as serialized dict """
        item = Item(type='plain_text', data=dict(prop='value'))
        data = item.to_dict(serialized=True)
        self.assertTrue(type(data['meta']['created']) is str)

    def test_get_db_representation(self):
        """ Getting db representation of an item """
        item = Item(type='plain_text', data=dict(body='value'))
        result = item.to_db()
        self.assertTrue(type(result['fields']) is str)

    def test_raise_when_setting_non_dictionary_data(self):
        """ Raise when setting a payload that is not a dict """
        item = Item(type='plain_text')
        with self.assertRaises(x.ItemError) as cm:
            item.fields = [123]

        self.assertIn('Fields must be a dictionary', str(cm.exception))

    def test_raise_when_fails_to_decode_data_string(self):
        """ Raise when data string can not be decoded """
        item = Item(type='plain_text')
        with self.assertRaises(x.ItemError) as cm:
            item.fields = 'no-a-json-string'
        self.assertIn('Failed to decode fields string', str(cm.exception))

    def test_getting_item_data(self):
        """ Getting event payload """
        item = Item(type="plain_text")
        self.assertTrue(type(item.fields) is dict)

    def test_getting_data_field(self):
        """ Getting data fields directly  """
        data = dict(
            id=1234,
            author='1234',
            object_id='12345-67890',
            fields=dict(
                body='I have some body text'
            )
        )

        item = Item(type='plain_text', **data)
        self.assertEquals(data['fields']['body'], item.body)

    def test_setting_data_field(self):
        """ Setting data fields """
        item = Item(type='plain_text')
        item.body = 'some value'
        self.assertEquals('some value', item.fields['body'])
        self.assertEquals('some value', item.body)

