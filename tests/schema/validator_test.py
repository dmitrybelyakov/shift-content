from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent.schema.validator import DefinitionSchema
from shiftcontent.schema.validator import TypeSchema
from shiftcontent.schema.validator import FieldSchema
from shiftcontent.schema.validator import FilterSchema
from shiftcontent.schema.validator import ValidatorSchema


@attr('schema', 'definition')
class DefinitionSchemaTest(BaseTestCase):

    def test_create_definition_schema(self):
        """ Instantiating definition schema"""
        schema = DefinitionSchema()
        self.assertIsInstance(schema, DefinitionSchema)

    def test_type_content(self):
        """ Type content test """
        schema = DefinitionSchema()
        result = schema.process(dict())
        errors = result.get_messages()
        self.assertFalse(result)
        self.assertIn('content', errors)
        self.assertIn(
            'Content types can\'t be empty',
            errors['content']['direct']
        )


@attr('schema', 'type')
class TypeSchemaTest(BaseTestCase):

    def test_create_type_schema(self):
        """ Instantiating type schema"""
        schema = TypeSchema()
        self.assertIsInstance(schema, TypeSchema)

    def test_type_name(self):
        """ Type name test """
        definition = dict(name='   Type Name   ')
        schema = TypeSchema()
        schema.process(definition)
        self.assertEquals(definition['name'], 'Type Name')

        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Content type must have a name', errors['name'])

    def test_content_type_names_are_unique(self):
        """ Content type names must be unique """
        definition = dict(name='Content Type')
        context = dict(content=[definition, definition])
        schema = TypeSchema()
        result = schema.process(definition, context)
        errors = result.get_messages()
        self.assertIn('is not unique', errors['name'][0])

    def test_type_handle(self):
        """ Type handle test """
        definition = dict(handle='   TYPE_HANDLE   ')
        schema = TypeSchema()
        schema.process(definition)
        self.assertEquals(definition['handle'], 'TYPE_HANDLE')

        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Content type must have a handle', errors['handle'])

    def test_type_handle_name_convention(self):
        """ Type handle must conform to naming conventions"""
        definition = dict(handle='1inv@lid')
        schema = TypeSchema()
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertIn('handle', errors)

        definition = dict(handle='valid_handle')
        schema = TypeSchema()
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertNotIn('handle', errors)

    def test_type_handles_are_unique(self):
        """ Type handles are unique """
        definition = dict(handle='type_handle')
        context = dict(content=[definition, definition])
        schema = TypeSchema()
        result = schema.process(definition, context)
        errors = result.get_messages()
        self.assertIn('is not unique', errors['handle'][0])

    def test_type_description(self):
        """ Type description test """
        definition = dict(description='   TYPE DESCRIPTION   ')
        schema = TypeSchema()
        schema.process(definition)
        self.assertEquals(definition['description'], 'TYPE DESCRIPTION')

        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Content type needs a description', errors['description'])

    def test_type_editor(self):
        """ Content type editor test"""
        definition = dict(editor='   some.module   ')
        schema = TypeSchema()
        schema.process(definition)
        self.assertEquals(definition['editor'], 'some.module')

    def test_type_editor_is_importable(self):
        """ Content type editor is importable """
        definition = dict(editor='shiftschema.schema.Schema')
        schema = TypeSchema()
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertNotIn('editor', errors)

        definition = dict(editor='not.importable.Something')
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertIn('editor', errors)

    def test_type_fields(self):
        """ Content type fields test """
        definition = dict(fields=None)
        schema = TypeSchema()
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertIn(
            'Content type must have fields',
            errors['fields']['direct']
        )


@attr('schema', 'field')
class FieldSchemaTest(BaseTestCase):

    def test_create_field_schema(self):
        """ Instantiating field schema"""
        schema = FieldSchema()
        self.assertIsInstance(schema, FieldSchema)

    def test_field_name(self):
        """ Field name test """
        self.fail('Implement me!')

    def test_field_handle(self):
        """ Filed handle test """
        self.fail('Implement me!')

    def test_field_description(self):
        """ Field description test """
        self.fail('Implement me!')

    def test_field_type(self):
        """ Field type test """
        self.fail('Implement me!')


@attr('schema', 'filter')
class FilterSchemaTest(BaseTestCase):

    def test_create_filter_schema(self):
        """ Instantiating filter schema"""
        schema = FilterSchema()
        self.assertIsInstance(schema, FilterSchema)

    def test_filter_type(self):
        """ Filter type test """
        self.fail('Implement me!')

    def test_filter_type_class_is_importable(self):
        """ Filter type class is importable """
        self.fail('Implement me!')


@attr('schema', 'validator')
class ValidatorSchemaTest(BaseTestCase):

    def test_create_validator_schema(self):
        """ Instantiating validatoe schema"""
        schema = ValidatorSchema()
        self.assertIsInstance(schema, ValidatorSchema)

    def test_validator_type(self):
        """ Validator type test """
        self.fail('Implement me!')

    def test_validator_type_class_is_importable(self):
        """ Validator type class is importable """
        self.fail('Implement me!')
