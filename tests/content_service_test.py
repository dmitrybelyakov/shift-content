from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from datetime import datetime
from shiftcontent import exceptions as x
from shiftcontent import ContentService
from shiftcontent.item import Item
from shiftcontent import SchemaService
from shiftevent.event_service import EventService
from shiftcontent.handlers import content_handlers


@attr('content', 'service')
class ContentServiceTest(BaseTestCase):

    # --------------------------------------------------------------------------
    # helpers & setuo
    # --------------------------------------------------------------------------

    def get_service(self):
        """ Configures and returns content service"""
        content_service = ContentService(
            db=self.db,
            event_service=EventService(db=self.db, handlers=content_handlers),
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
            data='{"data": "field"}'
        )

        # insert
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        service = self.get_service()
        item = service.get_item(object_id=object_id)
        self.assertIsInstance(item, Item)

    @attr('xxx')
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

