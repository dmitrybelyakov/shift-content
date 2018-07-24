from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent.definition_schema.schema import DefinitionSchema
from shiftcontent.definition_schema.schema import TypeSchema
from shiftcontent.definition_schema.schema import FieldSchema
from shiftcontent.definition_schema.schema import FilterSchema
from shiftcontent.definition_schema.schema import ValidatorSchema


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
        result = schema.process(definition, context=context)
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
        result = schema.process(definition, context=context)
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
        definition = dict(name='   Field Name   ')
        schema = FieldSchema()
        schema.process(definition)
        self.assertEquals('Field Name', definition['name'])

        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Field requires a name', errors['name'])

    def test_field_names_are_unique(self):
        """ Field names are unique within type """
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
        schema = FieldSchema()
        result = schema.process(field, context=definition)
        errors = result.get_messages()
        self.assertFalse(result)
        self.assertIn('name', errors)

    def test_field_handle(self):
        """ Filed handle test """
        definition = dict(handle='   field_handle   ')
        schema = FieldSchema()
        schema.process(definition)
        self.assertEquals('field_handle', definition['handle'])

        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Field requires a handle', errors['handle'])

    def test_field_handle_name_convention(self):
        """ Field handles conform to naming conventions """
        definition = dict(handle='1inv@lid')
        schema = FieldSchema()
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertIn('handle', errors)

        definition = dict(handle='valid_handle')
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertNotIn('handle', errors)

    def test_field_handles_are_unique(self):
        """ Field handles are unique within type """
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
        schema = FieldSchema()
        result = schema.process(field, context=definition)
        errors = result.get_messages()
        self.assertFalse(result)
        self.assertIn('handle', errors)

    def test_field_description(self):
        """ Field description test """
        definition = dict(description='   some description   ')
        schema = FieldSchema()
        schema.process(definition)
        self.assertEquals('some description', definition['description'])

    def test_field_type(self):
        """ Field type test """
        definition = dict(type='   field_type   ')
        schema = FieldSchema()
        schema.process(definition)
        self.assertEquals('field_type', definition['type'])

        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Field requires a type', errors['type'])


@attr('schema', 'filter')
class FilterSchemaTest(BaseTestCase):

    def test_create_filter_schema(self):
        """ Instantiating filter schema"""
        schema = FilterSchema()
        self.assertIsInstance(schema, FilterSchema)

    def test_filter_type(self):
        """ Filter type test """
        schema = FilterSchema()
        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Filter requires a type', errors['type'])

    def test_filter_type_class_is_importable(self):
        """ Filter type class is importable """
        schema = FilterSchema()
        definition = dict(type='shiftschema.filters.Strip')
        result = schema.process(definition)
        self.assertTrue(result)

        definition = dict(type='shiftschema.filters.Strips')
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertIn('is not importable', errors['type'][0])

    def test_filter_is_instantiatable(self):
        """ Filters are instantiatable """
        schema = FilterSchema()
        result = schema.validate(dict(
            type='shiftschema.filters.Linkify',
            crap=True
        ))
        err = result.get_messages()
        self.assertFalse(result)
        self.assertIn('type', err)
        self.assertIn('is not instantiatable', err['type'][0])

        result = schema.validate(dict(
            type='shiftschema.filters.Linkify',
            parse_email=True
        ))
        self.assertTrue(result)


@attr('schema', 'validator')
class ValidatorSchemaTest(BaseTestCase):

    def test_create_validator_schema(self):
        """ Instantiating validatoe schema"""
        schema = ValidatorSchema()
        self.assertIsInstance(schema, ValidatorSchema)

    def test_validator_type(self):
        """ Validator type test """
        schema = ValidatorSchema()
        result = schema.process(dict())
        errors = result.get_messages()
        self.assertIn('Validator requires a type', errors['type'])

    def test_validator_type_class_is_importable(self):
        """ Validator type class is importable """
        schema = ValidatorSchema()
        definition = dict(type='shiftschema.validators.Required')
        result = schema.process(definition)
        self.assertTrue(result)

        definition = dict(type='shiftschema.validators.Requiredz')
        result = schema.process(definition)
        errors = result.get_messages()
        self.assertIn('is not importable', errors['type'][0])

    def test_validator_is_instantiatable(self):
        """ Validators are instantiatable """
        schema = ValidatorSchema()
        result = schema.validate(dict(
            type='shiftschema.validators.Required',
            crap=True
        ))
        err = result.get_messages()
        self.assertFalse(result)
        self.assertIn('type', err)
        self.assertIn('is not instantiatable', err['type'][0])

        result = schema.validate(dict(
            type='shiftschema.validators.Required',
            allow_zero=True
        ))
        self.assertTrue(result)

