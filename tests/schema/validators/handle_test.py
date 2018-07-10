from tests.base import BaseTestCase
from nose.plugins.attrib import attr


from shiftcontent.schema.validators import Handle


@attr('schema', 'validators', 'handle')
class HandleTest(BaseTestCase):

    def test_instantiate_handle_validator(self):
        """ Instantiating handle validator """
        validator = Handle()
        self.assertIsInstance(validator, Handle)

    def test_valid_handle_passes_validation(self):
        """ Valid type/field handle passes validation """
        validator = Handle()
        handle = 'valid_handle'
        error = validator.validate(handle)
        self.assertFalse(error)

    def test_invalid_handle_fails_validation(self):
        """ Invalid handle fails validation """
        invalid = [
            '1starts_with_number',
            'NOT_LOWERCASE',
            'contains spaces',
            'contains-hyphen',
            'or other illegal characters !@#$*&^*,+'
        ]

        validator = Handle()
        for handle in invalid:
            error = validator.validate(handle)
            self.assertTrue(error)

