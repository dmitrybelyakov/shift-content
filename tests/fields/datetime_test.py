from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from datetime import datetime

from shiftcontent.fields import DateTime


@attr('fields', 'field_datetime')
class DatetimeTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating datetime field """
        field = DateTime()
        self.assertIsInstance(field, DateTime)

    def test_setting_value_from_string(self):
        """ Setting datetime field from string """
        value = '2020-10-18 16:40:22'
        field = DateTime(value)
        self.assertTrue(type(field.get()) is datetime)

    def test_setting_value_from_datetime(self):
        """ Setting datetime field from datetime """
        field = DateTime(datetime.utcnow())
        self.assertTrue(type(field.get()) is datetime)

    def test_get_value(self):
        """ Getting value from datetime field """
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTime(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is datetime)

    def test_get_db_representation(self):
        """ Getting db representation of datetime field value """
        value = '2020-10-18 16:40:22'
        field = DateTime(value)
        self.assertEquals(value, field.to_db())
        self.assertTrue(type(field.to_db()) is str)

    def test_populate_from_db(self):
        """ Populating value from db representation for datetime field """
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTime()
        field.from_db(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is datetime)

    def test_get_json_representation(self):
        """ Getting json representation of datetime field value """
        value = '2020-10-18 16:40:22'
        field = DateTime(value)
        self.assertEquals(value, field.to_json())
        self.assertTrue(type(field.to_json()) is str)

    def test_populate_from_json(self):
        """ Populating value from json representation for datetime field """
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTime()
        field.from_json(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is datetime)

    def test_get_search_representation(self):
        """ Getting search representation of datetime field value """
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTime(value)
        self.assertEquals(value, field.to_search().strftime(fmt))
        self.assertTrue(type(field.to_search()) is datetime)

    def test_get_search_mapping(self):
        """ Getting search index data type for the datetime field """
        field = DateTime()
        self.assertEquals('date', field.search_mapping())





