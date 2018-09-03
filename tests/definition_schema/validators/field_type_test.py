from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from pprint import pprint as pp

from shiftcontent.definition_schema.validators import FieldType


@attr('schema', 'validators', 'field_type')
class FieldTypeTest(BaseTestCase):

    def test_instantiate_handle_validator(self):
        """ Instantiating field type validator """
        validator = FieldType()
        self.assertIsInstance(validator, FieldType)

    def test_existing_type_passes_validation(self):
        """ Existing field type passes validation """
        validator = FieldType()
        field_type = 'text'
        error = validator.validate(field_type)
        self.assertFalse(error)

    def test_nonexistent_type_fails_validation(self):
        """ Nonexistent field type fails validation """
        validator = FieldType()
        field_type = 'nonexistent'
        error = validator.validate(field_type)
        self.assertTrue(error)


