from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item_schema import BaseItemSchema
from shiftcontent.schema_service import SchemaService
from pprint import pprint as pp


@attr('item', 'schema')
class DefaultItemSchemaTest(BaseTestCase):

    def test_create_default_schema(self):
        """ Creating default content item schema """
        schema = BaseItemSchema()
        self.assertIsInstance(schema, BaseItemSchema)

    def test_id_field(self):
        """ Default item schema: id field"""
        schema = BaseItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('id', result.get_messages())

    def test_author_field(self):
        """ Default item schema: author field"""
        schema = BaseItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('author', result.get_messages())

    def test_type_field(self):
        """ Default item schema: type field"""
        schema = BaseItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('type', result.get_messages())

    def test_type_must_exist(self):
        """ Default item schema: content type must exist """
        schema_service = SchemaService(self.schema_path, self.revisions_path)
        context = dict(
            content_schema=schema_service.schema
        )

        data = dict(
            id='123',
            author='Joe Blow',
            object_id='123-456-789',
            type='nonexistent'
        )

        schema = BaseItemSchema()
        result = schema.process(model=data, context=context)
        err = result.get_messages()
        self.assertIn('type', err)
        self.assertIn('does not exist.', err['type'][0])

    def test_object_id_field(self):
        """ Default item schema: object id field"""
        schema = BaseItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('object_id', result.get_messages())
