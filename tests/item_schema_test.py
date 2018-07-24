from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item_schema import UpdateItemSchema
from shiftcontent.definition_service import DefinitionService
from pprint import pprint as pp


@attr('item', 'schema')
class ItemSchemaTest(BaseTestCase):

    def test_create_default_schema(self):
        """ Creating default content item schema """
        schema = UpdateItemSchema()
        self.assertIsInstance(schema, UpdateItemSchema)

    def test_id_field(self):
        """ Default item schema: id field"""
        schema = UpdateItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('id', result.get_messages())

    def test_author_field(self):
        """ Default item schema: author field"""
        schema = UpdateItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('author', result.get_messages())

    def test_type_field(self):
        """ Default item schema: type field"""
        schema = UpdateItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('type', result.get_messages())

    def test_type_must_exist(self):
        """ Default item schema: content type must exist """
        definition_service = DefinitionService(
            self.definition_path,
            self.revisions_path
        )

        context = dict(
            definition=definition_service.definition
        )

        data = dict(
            id='123',
            author='Joe Blow',
            object_id='123-456-789',
            type='nonexistent'
        )

        schema = UpdateItemSchema()
        result = schema.process(model=data, context=context)
        err = result.get_messages()
        self.assertIn('type', err)
        self.assertIn('does not exist.', err['type'][0])

    def test_object_id_field(self):
        """ Default item schema: object id field"""
        schema = UpdateItemSchema()
        result = schema.process(dict())
        self.assertFalse(result)
        self.assertIn('object_id', result.get_messages())
