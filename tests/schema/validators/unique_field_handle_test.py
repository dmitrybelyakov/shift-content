from tests.base import BaseTestCase
from nose.plugins.attrib import attr


from shiftcontent.schema.validators import UniqueFieldHandle


@attr('schema', 'validators', 'unique_field_handle')
class UniqueTypeNameTest(BaseTestCase):

    def test_instantiate_unique_field_handle_validator(self):
        """ Instantiating unique field handle validator """
        validator = UniqueFieldHandle()
        self.assertIsInstance(validator, UniqueFieldHandle)

    def test_non_unique_field_handle_fails_validation(self):
        """ Non-unique content field handle fails validation """
        field = dict(
            name='Body',
            handle='body',
            type='text'
        )
        definition = dict(
            name='Text',
            handle='text',
            description='some description',
            editor='shiftcontent.editor.Editor',
            fields=[field, field]
        )

        validator = UniqueFieldHandle()
        error = validator.validate(field['handle'], context=definition)
        self.assertTrue(error)

    def test_unique_content_field_handle_passes_validation(self):
        """ Unique content field handle passes validation """
        field1 = dict(
            name='Title',
            handle='title',
            type='text'
        )
        field2 = dict(
            name='Body',
            handle='body',
            type='text'
        )
        definition = dict(
            name='Text',
            handle='text',
            description='some description',
            editor='shiftcontent.editor.Editor',
            fields=[field1, field2]
        )

        validator = UniqueFieldHandle()
        error = validator.validate(field1['handle'], context=definition)
        self.assertFalse(error)
