from tests.base import BaseTestCase
from nose.plugins.attrib import attr


from shiftcontent.schema.validators import UniqueTypeName


@attr('schema', 'validators', 'unique_type_name')
class UniqueTypeNameTest(BaseTestCase):

    def test_instantiate_unique_type_name_validator(self):
        """ Instantiating unique type name validato """
        validator = UniqueTypeName()
        self.assertIsInstance(validator, UniqueTypeName)

    def test_non_unique_type_name_fails_validation(self):
        """ Non-unique content type name fails validation """
        definition = {'content': [
            {
                'name': 'Markdown',
            },
            {
                'name': 'Markdown',
            },
        ]}

        validator = UniqueTypeName()
        error = validator.validate('Markdown', context=definition)
        self.assertTrue(error)


    def test_unique_content_type_name_passes_validation(self):
        """ Unique content type name passes validation """
        definition = {'content': [
            {
                'name': 'Markdown1',
            },
            {
                'name': 'Markdown2',
            },
        ]}

        validator = UniqueTypeName()
        error = validator.validate('Markdown1', context=definition)
        self.assertFalse(error)
