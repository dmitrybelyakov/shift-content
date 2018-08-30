from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.fields import Text


@attr('fields', 'field_text')
class TextTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating text field """
        field = Text()
        self.assertIsInstance(field, Text)

    def test_get_value(self):
        """ Getting value from text field """
        value = 'i am field value'
        field = Text(value)
        self.assertEquals(value, field.get())
        self.assertTrue(type(field.get()) is str)

    def test_get_db_representation(self):
        """ Getting db representation of text field value """
        value = 'i am field value'
        field = Text(value)
        self.assertEquals(value, field.to_db())
        self.assertTrue(type(field.to_db()) is str)

    def test_populate_from_db(self):
        """ Populating value from db representation for text field"""
        value = 'i am field value'
        field = Text()
        field.from_db(value)
        self.assertEquals(value, field.get())
        self.assertTrue(type(field.to_db()) is str)

    def test_get_json_representation(self):
        """ Getting json representation of text field value """
        value = 'i am field value'
        field = Text(value)
        self.assertEquals(value, field.to_json())
        self.assertTrue(type(field.to_json()) is str)

    def test_populate_from_json(self):
        """ Populating value from json representation for text field"""
        value = 'i am field value'
        field = Text()
        field.from_json(value)
        self.assertEquals(value, field.get())
        self.assertTrue(type(field.to_db()) is str)

    def test_get_search_representation(self):
        """ Getting search representation of text field value """
        value = 'i am field value'
        field = Text(value)
        self.assertEquals(value, field.to_search())
        self.assertTrue(type(field.to_search()) is str)

    def test_get_search_mapping(self):
        """ Getting search index data type for the text field """
        field = Text()
        self.assertEquals('text', field.search_mapping())





