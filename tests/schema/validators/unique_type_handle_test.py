from tests.base import BaseTestCase
from nose.plugins.attrib import attr


from shiftcontent.schema.validators import UniqueTypeHandle


@attr('schema', 'validators', 'unique_type_handle')
class UniqueTypeHandleTest(BaseTestCase):

    def test_instantiate_unique_type_name_validator(self):
        """ Instantiating unique type name validato """
        validator = UniqueTypeHandle()
        self.assertIsInstance(validator, UniqueTypeHandle)

    def test_non_unique_type_handle_fails_validation(self):
        """ Non-unique content type handle fails validation """
        definition = {'content': [
            {
                'handle': 'markdown',
            },
            {
                'handle': 'markdown',
            },
        ]}

        validator = UniqueTypeHandle()
        error = validator.validate('markdown', context=definition)
        self.assertTrue(error)

    def test_unique_content_type_name_passes_validation(self):
        """ Unique content type name passes validation """
        definition = {'content': [
            {
                'handle': 'markdown1',
            },
            {
                'handle': 'markdown2',
            },
        ]}

        validator = UniqueTypeHandle()
        error = validator.validate('markdown1', context=definition)
        self.assertFalse(error)
