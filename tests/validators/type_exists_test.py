from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.validators import TypeExists
from shiftcontent.definition_service import DefinitionService
from pprint import pprint as pp


@attr('item', 'vaidator', 'type_exists')
class ContentTypeExistsTest(BaseTestCase):

    def test_creating_validator(self):
        """ Creating content type existence validator """
        validator = TypeExists()
        self.assertIsInstance(validator, TypeExists)

    def test_existing_type_passes(self):
        """ Existing content type passes validation """
        definition_service = DefinitionService(
            self.definition_path,
            self.revisions_path
        )
        context = dict(definition=definition_service.definition)
        validator = TypeExists()
        error = validator.validate('markdown', context=context)
        self.assertFalse(error)

    def test_nonexistent_type_fails(self):
        """ Nonexistent content type fails validation """
        definition_service = DefinitionService(
            self.definition_path,
            self.revisions_path
        )
        context = dict(definition=definition_service.definition)
        validator = TypeExists()
        error = validator.validate('nonexistent', context=context)
        self.assertTrue(error)
