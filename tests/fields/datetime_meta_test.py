from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from datetime import datetime

from shiftcontent.fields import DateTimeMetaField


@attr('fields', 'field_datetime_meta')
class DatetimeMetaFieldTest(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating datetime meta field """
        field = DateTimeMetaField()
        self.assertIsInstance(field, DateTimeMetaField)

    def test_get_db_representation(self):
        """ Getting db representation of datetime meta field value """
        value = '2020-10-18 16:40:22'
        fmt = '%Y-%m-%d %H:%M:%S'
        field = DateTimeMetaField(value)
        self.assertEquals(value, field.get().strftime(fmt))
        self.assertTrue(type(field.get()) is datetime)





