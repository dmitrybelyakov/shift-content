from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from datetime import datetime, date

from shiftcontent.fields import Date


@attr('fields', 'field_date')
class DateTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating date field """
        field = Date()
        field.set(None)
        self.assertIsInstance(field, Date)

    def test_setting_value_from_string(self):
        """ Setting date field from string """
        value = '2020-10-18'
        field = Date(value)
        self.assertTrue(type(field.get()) is date)

    def test_setting_value_from_datetime(self):
        """ Setting date field from datetime """
        value = date.today()
        field = Date(value)
        self.assertTrue(type(field.get()) is date)

    def test_get_value(self):
        """ Getting value from date field """
        value = '2020-10-18'
        fmt = '%Y-%m-%d'
        field = Date(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is date)

    def test_get_db_representation(self):
        """ Getting db representation of date field value """
        value = '2020-10-18'
        field = Date(value)
        self.assertEquals(value, field.to_db())
        self.assertTrue(type(field.to_db()) is str)

    def test_populate_from_db(self):
        """ Populating value from db representation for date field """
        value = '2020-10-18'
        fmt = '%Y-%m-%d'
        field = Date()
        field.from_db(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is date)

    def test_get_json_representation(self):
        """ Getting json representation of date field value """
        value = '2020-10-18'
        field = Date(value)
        self.assertEquals(value, field.to_json())
        self.assertTrue(type(field.to_json()) is str)

    def test_populate_from_json(self):
        """ Populating value from json representation for date field """
        value = '2020-10-18'
        fmt = '%Y-%m-%d'
        field = Date()
        field.from_json(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is date)

    def test_get_search_representation(self):
        """ Getting search representation of date field value """
        value = '2020-10-18'
        fmt = '%Y-%m-%d'
        field = Date(value)
        self.assertEquals(value, field.to_search().strftime(fmt))
        self.assertTrue(type(field.to_search()) is date)

    def test_get_search_mapping(self):
        """ Getting search index data type for the datetime field """
        field = Date()
        mapping = field.search_mapping()
        self.assertEquals('date', mapping['type'])





