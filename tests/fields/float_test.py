from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.fields import Float


@attr('fields', 'field_float')
class FloatTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating float field """
        field = Float()
        field.set(None)
        self.assertIsInstance(field, Float)

    def test_get_value(self):
        """ Getting value from float field """
        value = '-5.0'
        field = Float(value)
        self.assertEquals(-5.0, field.get())
        self.assertTrue(type(field.get()) is float)

    def test_get_db_representation(self):
        """ Getting db representation of float field value """
        value = '-5.0'
        field = Float(value)
        self.assertEquals(-5.0, field.to_db())
        self.assertTrue(type(field.to_db()) is float)

    def test_populate_from_db(self):
        """ Populating value from db representation for float field"""
        value = '-5.0'
        field = Float()
        field.from_db(value)
        self.assertEquals(-5.0, field.get())
        self.assertTrue(type(field.get()) is float)

    def test_get_json_representation(self):
        """ Getting json representation of float field value """
        value = '-5.0'
        field = Float(value)
        self.assertEquals(-5.0, field.to_json())
        self.assertTrue(type(field.to_json()) is float)

    def test_populate_from_json(self):
        """ Populating value from json representation for float field"""
        value = '-5.0'
        field = Float()
        field.from_json(value)
        self.assertEquals(-5.0, field.get())
        self.assertTrue(type(field.get()) is float)

    def test_get_search_representation(self):
        """ Getting search representation of float field value """
        value = '-5.0'
        field = Float(value)
        self.assertEquals(-5.0, field.to_search())
        self.assertTrue(type(field.to_search()) is float)

    def test_get_search_mapping(self):
        """ Getting search index data type for the float field """
        field = Float()
        self.assertEquals('double', field.search_mapping())





