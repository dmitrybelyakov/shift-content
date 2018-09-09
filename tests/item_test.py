from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item import Item
from shiftcontent import exceptions as x
from datetime import datetime
from uuid import uuid1
import json
from pprint import pprint as pp


@attr('item')
class ItemTest(BaseTestCase):

    def test_instantiating_item(self):
        """ Instantiating item """
        item = Item()
        self.assertIsInstance(item, Item)

    def test_can_access_field_types(self):
        """ Content item has access to field types """
        item = Item()
        types = item.field_types
        self.assertTrue(type(types) is dict)

    def test_getting_printable_representation_of_item(self):
        """ Getting printable representation of an item """
        item = Item()
        repr = item.__repr__()
        self.assertIn('<ContentItem id=[None]', repr)

    def test_init_metafields_on_creation(self):
        """ Init metafields when initializing item """
        item = Item()
        self.assertIsNotNone(item.fields)
        for metafield in item.metafields:
            self.assertIn(metafield, item.fields)

    def test_setting_fields(self):
        """ Setting fields on an item """
        item = Item()
        item.path = 123
        item.nonexistent = 'set on object'
        self.assertEquals('123', item.path)
        self.assertEquals('set on object', item.nonexistent)

    def test_setting_item_fields_to_none(self):
        """ Allow to set item fields to none """
        item = Item(type='plain_text')
        self.assertIsNone(item.path)
        self.assertIsNone(item.body)

        item.path = '1.2.3.4'
        item.body = 'hola!'
        self.assertIsNotNone(item.path)
        self.assertIsNotNone(item.body)

        # now set to None
        item.path = None
        item.body = None
        self.assertIsNone(item.path)
        self.assertIsNone(item.body)

    def test_setting_fields_with_setter(self):
        """ Setting fields on an item using setter method """
        item = Item()
        item.set_field('path', 123)
        item.set_field('nonexistent', 'silently pass')
        self.assertEquals('123', item.path)
        with self.assertRaises(AttributeError):
            print(item.nonexistent)

    def test_set_creation_date_on_creation(self):
        """ Setting creation date on item instantiation """
        item = Item()
        self.assertIsInstance(item.created, datetime)

    def test_set_creation_date_from_string(self):
        """ Set creation date on item from string value """
        item = Item()
        item.set_field('created', '2020-12-12 12:20:30', initial=True)
        self.assertIsInstance(item.created, datetime)

    def test_init_custom_fields_when_setting_type(self):
        """ Initialize custom fields when setting content type """
        item = Item()
        item.set_field('type', 'plain_text', initial=True)
        self.assertIn('type', item.fields)
        self.assertIn('body', item.fields)

    def test_throw_exception_when_setting_invalid_type(self):
        """ Unable to set nonexistent content type on an item """
        item = Item()
        with self.assertRaises(x.ItemError) as cm:
            item.set_field('type', 'nonexistent', initial=True)
        self.assertIn(
            'Unable to set content type: [nonexistent] is undefined',
            str(cm.exception)
        )

    def test_can_populate_from_kwargs(self):
        """ Populating from kwargs on instantiation """
        data = dict(
            body='Some content',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20',
            type='plain_text',
        )

        item = Item(**data)
        self.assertEquals(data['type'], item.type)
        self.assertEquals(data['body'], item.body)

    def test_unable_to_change_frozen_props(self):
        """ Unable to modify frozen properties of an item after creation """
        data = dict(
            body='Some content',
            author='author_id',
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20',
            type='plain_text',
        )

        item = Item(**data)
        item.author = 'UPDATED'
        self.assertEquals(data['author'], item.author)

    def test_item_to_dict(self):
        """ Getting dictionary representation of an item """
        item = Item()
        data = item.to_dict()
        self.assertTrue(type(data) is dict)

    def test_can_populate_from_dict(self):
        """ Populating item from dict """
        data = dict(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )

        item = Item()
        item.from_dict(data, initial=True)
        self.assertEquals(data['id'], item.id)
        self.assertEquals(data['type'], item.type)
        self.assertEquals(data['body'], item.body)

    def test_skip_frozen_props_when_populating_from_dict(self):
        """ Skip frozen properties when populating item from dict """
        initial_data = dict(
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )
        item = Item(**initial_data)

        updated_data = dict(
            type='markdown',
            author=456,
            body='Updated data'
        )
        item.from_dict(updated_data)

        self.assertNotEquals(updated_data['type'], item.type)
        self.assertNotEquals(updated_data['author'], item.type)
        self.assertEquals(updated_data['body'], item.body)

    def test_item_to_db(self):
        """ Getting databse representation of an item """
        item = Item(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )

        db_repr = item.to_db()
        self.assertTrue(type(db_repr) is dict)
        self.assertTrue(type(db_repr['fields']) is str)
        self.assertNotIn('type', db_repr)
        self.assertNotIn('id', db_repr)
        self.assertNotIn('object_id', db_repr)
        self.assertNotIn('author', db_repr)
        self.assertNotIn('created', db_repr)
        self.assertIn('path', db_repr)
        self.assertIn('fields', db_repr)

    def test_item_to_db_initial(self):
        """ Getting database representation of an item for initial creation """
        item = Item(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )
        db_repr = item.to_db(update=False)
        self.assertIn('type', db_repr)
        self.assertIn('id', db_repr)
        self.assertIn('object_id', db_repr)
        self.assertIn('author', db_repr)
        self.assertIn('created', db_repr)
        self.assertIn('path', db_repr)
        self.assertIn('fields', db_repr)

    def test_item_from_db(self):
        """ Populate item back from db data and decode json fields """
        item = Item(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )

        db_repr = item.to_db(update=False)
        restored = Item()
        restored.from_db(db_repr)
        self.assertEquals(item.id, restored.id)
        self.assertEquals(item.type, restored.type)
        self.assertEquals(item.body, restored.body)

    def test_item_to_search(self):
        """ Item returns a  json document to put to index"""
        item = Item(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )
        search_repr = item.to_search()
        self.assertTrue(type(search_repr) is dict)

    def test_item_to_json(self):
        """ Can convert item to json """
        item = Item(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )

        to_json = item.to_json(as_string=False)
        self.assertTrue(type(to_json) is dict)
        self.assertTrue(type(to_json['created']) is str)

        to_json = item.to_json()
        self.assertTrue(type(to_json) is str)

    def test_item_from_json(self):
        """ Populate item from json """
        item = Item(
            id=999,
            body='Some content',
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            created='2018-12-12 12:20:20'
        )

        json_data = item.to_json()
        restored = Item()
        restored.from_json(json_data)
        self.assertEquals(item.id, restored.id)
        self.assertEquals(item.type, restored.type)
        self.assertEquals(item.body, restored.body)

    def test_raise_when_populating_from_bad_json(self):
        """ Raise error if json decode fails when populating from json"""
        item = Item()
        with self.assertRaises(x.ItemError) as cm:
            item.from_json('bad json data')
        self.assertIn('Failed to decode json', str(cm.exception))


