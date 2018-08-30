from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from datetime import datetime

from shiftcontent.fields import DateTimeMeta


@attr('fields', 'field_datetime_meta')
class DatetimeMetaFieldTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating datetime meta field """
        field = DateTimeMeta()
        self.assertIsInstance(field, DateTimeMeta)

    def test_get_db_representation(self):
        """ Getting db representation of datetime meta field value """
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTimeMeta(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is datetime)

    def test_populate_from_db(self):
        """ Populating from db representation for datetime meta field"""
        value = datetime.utcnow()
        field = DateTimeMeta()
        field.from_json(value)
        self.assertEquals(value, field.get())
        self.assertTrue(type(field.get()) is datetime)

    def test_populate_from_json(self):
        """ Populating from json representation for datetime meta field"""
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTimeMeta()
        field.from_json(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is datetime)
