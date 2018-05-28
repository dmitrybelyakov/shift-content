from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import ContentService
from shiftcontent import SchemaService
from shiftcontent import EventService


@attr('content', 'service')
class SchemaServiceTest(BaseTestCase):

    # --------------------------------------------------------------------------
    # helpers & setuo
    # --------------------------------------------------------------------------

    def get_service(self):
        """ Configures and returns content service"""
        content_service = ContentService(
            db=self.db,
            event_service=EventService(),
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




