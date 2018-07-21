from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.validators import TypeExists
from shiftcontent.schema_service import SchemaService
from pprint import pprint as pp


@attr('item', 'vaidator', 'type_exists')
class ContentTypeExistsTest(BaseTestCase):

    def test_creating_validator(self):
        """ Creating content type existence validator """
        validator = TypeExists()
        self.assertIsInstance(validator, TypeExists)

    def test_existing_type_passes(self):
        """ Existing content type passes validation """
        schema_service = SchemaService(self.schema_path, self.revisions_path)
        context = dict(content_schema=schema_service.schema)
        validator = TypeExists()
        error = validator.validate('markdown', context=context)
        self.assertFalse(error)

    def test_nonexistent_type_fails(self):
        """ Nonexistent content type fails validation """
        schema_service = SchemaService(self.schema_path, self.revisions_path)
        context = dict(content_schema=schema_service.schema)
        validator = TypeExists()
        error = validator.validate('nonexistent', context=context)
        self.assertTrue(error)
