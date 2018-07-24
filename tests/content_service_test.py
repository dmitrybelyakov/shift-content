from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from pprint import pprint as pp

from uuid import uuid1
from datetime import datetime
from shiftschema.schema import Result
from shiftcontent import db
from shiftcontent import content
from shiftcontent import exceptions as x
from shiftcontent.content_service import ContentService
from shiftcontent.item import Item
from shiftcontent.item_schema import UpdateItemSchema, CreateItemSchema


@attr('content', 'service')
class ContentServiceTest(BaseTestCase):

    # --------------------------------------------------------------------------
    # tests
    # --------------------------------------------------------------------------

    def test_create_content_service(self):
        """ Creating content service"""
        service = ContentService()
        self.assertIsInstance(service, ContentService)


    def test_creating_item_update_schema(self):
        """ Create schema for content item update """
        schema = content.item_schema('plain_text', 'update')
        self.assertIsInstance(schema, UpdateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_creating_item_create_schema(self):
        """ Create schema for content item creation """
        schema = content.item_schema('plain_text', 'create')
        self.assertIsInstance(schema, CreateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_raise_on_requesting_bad_schema_type(self):
        """ Item schema type can be either create or update """
        with self.assertRaises(x.InvalidItemSchemaType):
            content.item_schema('plain_text', 'BAD')

    def test_get_item(self):
        """ Getting item by object id """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created= datetime.utcnow(),
            object_id=object_id,
            type='plain_text',
            fields='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        item = content.get_item(object_id=object_id)
        self.assertIsInstance(item, Item)

    def test_fail_to_initialize_an_item_from_database_if_type_is_unknown(self):
        """ Fail to initialize item from database if type not in schema """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created=datetime.utcnow(),
            object_id=object_id,
            type='nonexistent',
            data='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        with self.assertRaises(x.UndefinedContentType) as cm:
            content.get_item(object_id=object_id)
        err = 'Database contains item (1) of undefined type [nonexistent]'
        self.assertIn(err, str(cm.exception))

    def test_create_content_item(self):
        """ Create a simple content item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content.create_item(author=author, content_type=type, data=data)
        self.assertEquals(1, item.id)

    def test_created_item_filtered(self):
        """ Incoming data is filtered with schema when creeating item """
        type = 'plain_text'
        author = 123
        data = dict(body='   I am a simple content item   ')
        item = content.create_item(author=author, content_type=type, data=data)
        self.assertEquals('I am a simple content item', item.body)

    def test_return_validation_result_when_creating_with_invalid_data(self):
        """ Return validation errors when creating item with bad data """
        # services.content.item_schema(content_type='markdown')
        type = 'plain_text'
        author = 123
        data = dict(body='')
        item = content.create_item(author=author, content_type=type, data=data)
        self.assertIsInstance(item, Result)
        err = item.get_messages()
        self.assertIn('body', err)
        self.assertEquals(2, len(err['body']))

    def test_raise_when_creating_an_item_of_undefined_type(self):
        """ Raise when creating content item of undefined type """
        with self.assertRaises(x.UndefinedContentType) as cm:
            content.create_item(author='123', content_type='BAD!', data={})

    def test_raise_on_deleting_nonexistent_item(self):
        """ Raise when attempting to delete nonexistent item """
        self.fail('Implement me!')

    def test_deleting_content_item(self):
        """ Deleting content item """
        self.fail('Implement me!')
