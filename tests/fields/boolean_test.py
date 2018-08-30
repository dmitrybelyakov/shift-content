from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.fields import Boolean


@attr('fields', 'field_boolean')
class BooleanTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating boolean field """
        field = Boolean()
        field.set(None)
        self.assertIsInstance(field, Boolean)

    def test_get_value(self):
        """ Getting value from boolean field """
        value = 0
        field = Boolean(value)
        self.assertFalse(field.get())
        self.assertTrue(type(field.get()) is bool)

    def test_get_db_representation(self):
        """ Getting db representation of boolean field value """
        value = 0
        field = Boolean(value)
        self.assertFalse(field.to_db())
        self.assertTrue(type(field.to_db()) is bool)

    def test_populate_from_db(self):
        """ Populating value from db representation for boolean field"""
        value = '0'
        field = Boolean()
        field.from_db(value)
        self.assertFalse(field.get())
        self.assertTrue(type(field.get()) is bool)

    def test_get_json_representation(self):
        """ Getting json representation of boolean field value """
        value = 0
        field = Boolean(value)
        self.assertFalse(field.to_json())
        self.assertTrue(type(field.to_json()) is bool)

    def test_populate_from_json(self):
        """ Populating value from json representation for boolean field"""
        value = '1'
        field = Boolean()
        field.from_json(value)
        self.assertTrue(field.get())
        self.assertTrue(type(field.get()) is bool)

    def test_get_search_representation(self):
        """ Getting search representation of boolean field value """
        value = 0
        field = Boolean(value)
        self.assertFalse(field.to_search())
        self.assertTrue(type(field.to_search()) is bool)

    def test_get_search_mapping(self):
        """ Getting search index data type for the boolean field """
        field = Boolean()
        self.assertEquals('boolean', field.search_mapping())





