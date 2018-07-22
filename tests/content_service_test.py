from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from datetime import datetime
from shiftschema.schema import Schema
from shiftcontent import exceptions as x
from shiftcontent import ContentService
from shiftcontent.item import Item
from shiftcontent import SchemaService
from shiftevent.event_service import EventService
from shiftcontent.handlers import content_handlers
from shiftcontent.item_schema import UpdateItemSchema, CreateItemSchema
from shiftevent.db import Db as EventsDb


@attr('content', 'service')
class ContentServiceTest(BaseTestCase):

    # --------------------------------------------------------------------------
    # helpers & setuo
    # --------------------------------------------------------------------------

    def get_service(self):
        """ Configures and returns content service"""

        # IMPORTANT: we have to make sure the same content db instance is passed
        # to event service. It is what gets passed to event handlers as db, and
        # handlers have to have access to content tables

        content_service = ContentService(
            db=self.db,
            event_service=EventService(self.db, handlers=content_handlers),
            schema_service=SchemaService(self.schema_path, self.revisions_path)
        )
        return content_service

    # --------------------------------------------------------------------------
    # tests
    # --------------------------------------------------------------------------

    def test_create_content_service(self):
        """ Creating content service"""
        service = self.get_service()
        self.assertIsInstance(service, ContentService)

    def test_get_item(self):
        """ Getting item by object id """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created= datetime.utcnow(),
            object_id=object_id,
            type='plain_text',
            data='{"body": "some content"}'
        )

        # insert
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        service = self.get_service()
        item = service.get_item(object_id=object_id)
        self.assertIsInstance(item, Item)

    def test_fail_to_initialize_an_item_from_database_if_type_is_unknown(self):
        """ Fail to initialize item from database if type not in schema """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created= datetime.utcnow(),
            object_id=object_id,
            type='nonexistent',
            data='{"body": "some content"}'
        )

        # insert
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        service = self.get_service()
        with self.assertRaises(x.UndefinedContentType) as cm:
            service.get_item(object_id=object_id)
        err = 'Database contains item (1) of undefined type [nonexistent]'
        self.assertIn(err, str(cm.exception))

    @attr('zzz')
    def test_create_content_item(self):
        """ Create a simple content item """
        service = self.get_service()
        type = 'plain_text'
        author = 123
        data = dict(body='I am a simple content item')
        item = service.create_item(author=author, content_type=type, data=data)
        self.assertEquals(1, item.id)

    def test_raise_when_creating_an_item_of_undefined_type(self):
        """ Raise when creating content item of undefined type """
        service = self.get_service()
        with self.assertRaises(x.UndefinedContentType) as cm:
            service.create_item(author='123', content_type='BAD!', data={})

    def test_creating_item_update_schema(self):
        """ Create schema for content item update """
        service = self.get_service()
        schema = service.item_schema('plain_text', 'update')
        self.assertIsInstance(schema, UpdateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_creating_item_create_schema(self):
        """ Create schema for content item creation """
        service = self.get_service()
        schema = service.item_schema('plain_text', 'create')
        self.assertIsInstance(schema, CreateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_raise_on_requesting_bad_schema_type(self):
        """ Item schema type can be either create or update """
        service = self.get_service()
        with self.assertRaises(x.InvalidItemSchemaType):
            service.item_schema('plain_text', 'BAD')
