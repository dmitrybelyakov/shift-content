from tests.base import BaseTestCase
from nose.plugins.attrib import attr


from shiftcontent.schema.validators import UniqueFieldName


@attr('schema', 'validators', 'unique_field_name')
class UniqueTypeNameTest(BaseTestCase):

    def test_instantiate_unique_field_name_validator(self):
        """ Instantiating unique field name validator """
        validator = UniqueFieldName()
        self.assertIsInstance(validator, UniqueFieldName)

    def test_non_unique_field_name_fails_validation(self):
        """ Non-unique content field name fails validation """
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

        validator = UniqueFieldName()
        error = validator.validate(field['name'], context=definition)
        self.assertTrue(error)

    def test_unique_content_field_name_passes_validation(self):
        """ Unique content field name passes validation """
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

        validator = UniqueFieldName()
        error = validator.validate(field1['name'], context=definition)
        self.assertFalse(error)
