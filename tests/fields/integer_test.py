from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.fields import Integer


@attr('fields', 'field_integer')
class IntegerTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating integer field """
        field = Integer()
        self.assertIsInstance(field, Integer)

    def test_get_value(self):
        """ Getting value from integer field """
        value = 1.2
        field = Integer(value)
        self.assertEquals(1, field.get())
        self.assertTrue(type(field.get()) is int)

    def test_get_db_representation(self):
        """ Getting db representation of integer field value """
        value = 1.2
        field = Integer(value)
        self.assertEquals(1, field.to_db())
        self.assertTrue(type(field.to_db()) is int)

    def test_get_json_representation(self):
        """ Getting json representation of integer field value """
        value = 1.2
        field = Integer(value)
        self.assertEquals(1, field.to_json())
        self.assertTrue(type(field.to_json()) is int)

    def test_get_search_representation(self):
        """ Getting search representation of integer field value """
        value = 1.2
        field = Integer(value)
        self.assertEquals(1, field.to_search())
        self.assertTrue(type(field.to_search()) is int)

    def test_get_search_mapping(self):
        """ Getting search index data type for the integer field """
        field = Integer()
        self.assertEquals('long', field.search_mapping())





