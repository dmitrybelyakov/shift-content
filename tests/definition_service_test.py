from tests.base import BaseTestCase
from nose.plugins.attrib import attr

import os
import hashlib
import yaml
import json
from pprint import pprint as pp
from shiftcontent.definition_service import DefinitionService
from shiftcontent import exceptions as x


@attr('definition', 'service')
class DefinitionServiceTest(BaseTestCase):

    def test_create_definition_service(self):
        """ Creating definition service"""
        service = DefinitionService(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )
        self.assertIsInstance(service, DefinitionService)

    def test_create_revisions_directory_on_first_access(self):
        """ Create directory for definition revisions if does not exist """
        path = self.revisions_path
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=path
        )

        self.assertFalse(os.path.exists(path))
        self.assertTrue(os.path.exists(service.revisions_path))

    def test_registry_is_empty_if_no_file(self):
        """ Return empty dict if registry file does not exist"""
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )

        registry = service.revisions
        self.assertTrue(type(registry) is dict)
        self.assertFalse(registry)

    def test_load_parse_and_return_existing_registry(self):
        """ Existing registry can be loaded successfully into a dict"""
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )

        registry = {
            '91827219871298': {
                'definition_file': '102981209821.yml',
                'date': '2016-04-22 12:45:00'
            }
        }

        registry_json = json.dumps(registry, ensure_ascii=False, indent=4)
        registry_file = os.path.join(service.revisions_path, '_registry.yml')
        with open(registry_file, 'w') as file:
            file.write(registry_json)

        loaded_registry = service.revisions
        self.assertEquals(registry, loaded_registry)

    def test_raise_when_unable_to_find_definition(self):
        """ Raise exception when unable to find definition file"""
        service = DefinitionService()
        service.init(
            definition_path='/nothing/here',
            revisions_path=self.revisions_path
        )
        with self.assertRaises(x.ConfigurationException):
            service.load_definition()

    def test_raise_when_definition_fails_validation(self):
        """ Raise exception when definition fails validation"""
        invalid = {'content': [
            {
                'name': 'Markdown',
                'handle': 'markdown',
                'editor': 'shiftcontent.editor.Default',
                'fields': []
            },
        ]}

        path = os.path.join(self.tmp, 'invalid.yml')
        with open(path, 'w') as stream:
            yaml.dump(invalid, stream)

        service = DefinitionService()
        service.init(
            definition_path=path,
            revisions_path=self.revisions_path
        )

        with self.assertRaises(x.InvalidDefinition):
            service.load_definition()

    def test_ingest_valid_definition(self):
        """ Save definition file to revisions backlog """
        valid = {'content': [
            {
                'name': 'Markdown',
                'handle': 'markdown',
                'description': 'This is a markdown type',
                'editor': 'shiftcontent.editor.Editor',
                'fields': [
                    {
                        'name': 'Body',
                        'handle': 'body',
                        'description': 'body text',
                        'type': 'text',
                    }
                ]
            },
        ]}

        path = os.path.join(self.tmp, 'valid.yml')
        with open(path, 'w') as stream:
            yaml.dump(valid, stream)

        service = DefinitionService()
        service.init(
            definition_path=path,
            revisions_path=self.revisions_path
        )

        try:
            definition = service.definition
        except x.InvalidDefinition as err:
            print(err.validation_errors)

        with open(path) as yml:
            text = yml.read()

        # assert saved to backlog
        hash = hashlib.md5(str(text).encode('utf-8')).hexdigest()
        target = os.path.join(self.revisions_path, hash + '.yml')
        self.assertTrue(os.path.isfile(target))

        # assert saved to registry
        registry = service.revisions
        self.assertEquals(
            hash + '.yml',
            registry[list(registry.keys())[0]]['definition_file']
        )

    def test_abort_definition_revision_registering_if_no_file(self):
        """ Abort adding revision to registry if file not found """
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )

        with self.assertRaises(x.UnableToRegisterRevision):
            service.register_revision('nothing.yml')

    def test_can_register_definition_revision(self):
        """ Registering definition revision"""
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )

        path = service.revisions_path
        revision_file = os.path.join(path, 'randomhash.yml')
        with open(revision_file, 'w') as revision:
            revision.writelines(['revision yaml data'])

        service.register_revision('randomhash.yml')
        registry = service.revisions
        self.assertTrue(type(registry) is dict)
        self.assertEquals(1, len(registry.keys()))
        self.assertEquals(
            'randomhash.yml',
            registry[list(registry.keys())[0]]['definition_file']
        )

    def test_get_content_type_definition_by_handle(self):
        """ Getting content type definition by handle"""
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )

        type_definition = service.get_type('plain_text')
        self.assertTrue(type_definition)
        self.assertEquals('plain_text', type_definition['handle'])

    def test_raise_when_getting_type_definition_for_nonexistent_type(self):
        """ Raise when getting type definition for nonexistent type """
        service = DefinitionService()
        service.init(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )
        with self.assertRaises(x.UndefinedContentType) as cm:
            service.get_type('WOOPS')
        self.assertIn('Unable to find definition', str(cm.exception))
