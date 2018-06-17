from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import ContentService
from shiftcontent import SchemaService
from shiftcontent import EventService


@attr('content', 'service')
class ContentServiceTest(BaseTestCase):

    # --------------------------------------------------------------------------
    # helpers & setuo
    # --------------------------------------------------------------------------

    def get_service(self):
        """ Configures and returns content service"""
        content_service = ContentService(
            db=self.db,
            event_service=EventService(self.db),
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

