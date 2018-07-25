from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from pprint import pprint as pp

from uuid import uuid1
from datetime import datetime
from shiftschema.schema import Result
from shiftcontent import db
from shiftcontent import content_service
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
        schema = content_service.item_schema('plain_text', 'update')
        self.assertIsInstance(schema, UpdateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_creating_item_create_schema(self):
        """ Create schema for content item creation """
        schema = content_service.item_schema('plain_text', 'create')
        self.assertIsInstance(schema, CreateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_raise_on_requesting_bad_schema_type(self):
        """ Item schema type can be either create or update """
        with self.assertRaises(x.InvalidItemSchemaType):
            content_service.item_schema('plain_text', 'BAD')

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
        item = content_service.get_item(object_id=object_id)
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
            content_service.get_item(object_id=object_id)
        err = 'Database contains item (1) of undefined type [nonexistent]'
        self.assertIn(err, str(cm.exception))

    def test_create_content_item(self):
        """ Create a simple content item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )
        self.assertEquals(1, item.id)

    def test_created_item_filtered(self):
        """ Incoming data is filtered with schema when creeating item """
        type = 'plain_text'
        author = 123
        data = dict(body='   I am a simple content item   ')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )
        self.assertEquals('I am a simple content item', item.body)

    def test_return_validation_result_when_creating_with_invalid_data(self):
        """ Return validation errors when creating item with bad data """
        # services.content.item_schema(content_type='markdown')
        type = 'plain_text'
        author = 123
        data = dict(body='')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )
        self.assertIsInstance(item, Result)
        err = item.get_messages()
        self.assertIn('body', err)
        self.assertEquals(2, len(err['body']))

    def test_raise_when_creating_an_item_of_undefined_type(self):
        """ Raise when creating content item of undefined type """
        with self.assertRaises(x.UndefinedContentType):
            content_service.create_item(
                author='123',
                content_type='BAD!',
                data={}
            )

    def test_raise_on_deleting_nonexistent_item(self):
        """ Raise when attempting to delete nonexistent item """
        with self.assertRaises(x.ItemNotFound) as cm:
            content_service.delete_item(123, 123)
        self.assertIn(
            'Unable to delete nonexistent content item',
            str(cm.exception)
        )

    def test_deleting_content_item(self):
        """ Deleting content item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )
        object_id = item.object_id
        content_service.delete_item(author, item.object_id)

        with self.db.engine.begin() as conn:
            items = self.db.tables['items']
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNone(result)

    def test_raise_when_updating_item_of_bad_type(self):
        """ Fail to update item of bad type """
        with self.assertRaises(x.ItemError) as cm:
            content_service.update_item(author='12345', item=dict())
        self.assertIn('Update function expects', str(cm.exception))

    def test_raise_on_updating_nonexistent_item(self):
        """ test when trying to update nonexistent item """
        with self.assertRaises(x.ItemNotFound) as cm:
            item = Item(type='plain_text', author=123, body='I am a body')
            content_service.update_item(author=123, item=item)

        self.assertIn('Item must be saved first', str(cm.exception))

    def test_updating_content_item(self):
        """ Updating content item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )

        item.body = 'I am updated body'
        updated = content_service.update_item(author, item)
        self.assertEquals('I am updated body', updated.body)

    def test_return_validation_errors_if_updating_with_invalid_data(self):
        """ Validate data when updating content item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )

        item.body = '0'
        result = content_service.update_item(author, item)
        self.assertIsInstance(result, Result)
        self.assertFalse(result)
        self.assertIn('body', result.get_messages())

    def test_raise_on_updating_filed_for_nonexistent_item(self):
        """ Raise error when updating field on nonexistent item """
        with self.assertRaises(x.ItemNotFound) as cm:
            content_service.update_item_field(1, 'NONEXISTENT', 'body', '')
        self.assertIn('Unable to find item with such id', str(cm.exception))

    def test_raise_when_trying_to_update_nonexistent_field(self):
        """ Raise when updating nonexistent field on an item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )
        with self.assertRaises(x.ItemError) as cm:
            content_service.update_item_field(author, item.object_id, 'z', '')
        self.assertIn('is not allowed for content type', str(cm.exception))

    def test_return_errors_when_updating_item_field_with_bad_data(self):
        """ Validate data when updating item field"""
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )

        new_value = '0'
        result = content_service.update_item_field(
            author,
            item.object_id,
            'body',
            new_value
        )

        self.assertIsInstance(result, Result)
        self.assertFalse(result)
        self.assertIn('body', result.get_messages())

    def test_updating_content_item_field(self):
        """ Updating single field on content item """
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            data=data
        )

        new_value = 'NEW BODY VALUE'
        updated = content_service.update_item_field(
            author,
            item.object_id,
            'body',
            new_value
        )

        self.assertEquals(new_value, updated.body)

