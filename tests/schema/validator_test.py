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


@attr('schema', 'type')
class TypeSchemaTest(BaseTestCase):

    def test_create_type_schema(self):
        """ Instantiating type schema"""
        schema = TypeSchema()
        self.assertIsInstance(schema, TypeSchema)


@attr('schema', 'field')
class FieldSchemaTest(BaseTestCase):

    def test_create_field_schema(self):
        """ Instantiating field schema"""
        schema = FieldSchema()
        self.assertIsInstance(schema, FieldSchema)


@attr('schema', 'filter')
class FilterSchemaTest(BaseTestCase):

    def test_create_filter_schema(self):
        """ Instantiating filter schema"""
        schema = FilterSchema()
        self.assertIsInstance(schema, FilterSchema)


@attr('schema', 'validator')
class ValidatorSchemaTest(BaseTestCase):

    def test_create_validator_schema(self):
        """ Instantiating validatoe schema"""
        schema = ValidatorSchema()
        self.assertIsInstance(schema, ValidatorSchema)