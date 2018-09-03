from tests.base import BaseTestCase
from nose.plugins.attrib import attr

import os
import hashlib
import yaml
import json
import copy
import time
from pprint import pprint as pp
from frozendict import frozendict
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

    def test_get_field_types(self):
        """ Definition service has access to field types """
        service = DefinitionService(
            definition_path=self.definition_path,
            revisions_path=self.revisions_path
        )

        types = service.field_types()
        self.assertTrue(type(types) is dict)
        self.assertIn('text', types.keys())
        self.assertIn('integer', types.keys())
        self.assertIn('datetime', types.keys())

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
            definition = service.definition
        except x.InvalidDefinition as err:
            print(err.validation_errors)

        with open(path) as yml:
            text = yml.read()

        # assert returned frozen
        self.assertIsInstance(definition, frozendict)
        self.assertIsInstance(definition['markdown']['fields'][0], frozendict)

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

    def test_freeze_definition(self):
        """ Freezing content definition """
        data = {
            'content': [{
                'handle': 'markdown',
                'fields': [{
                    'handle': 'body',
                    'filters': [
                        {
                            'type': 'shiftcontent.filters.Strip'
                        },
                        {
                            'type': 'shiftcontent.filters.Lowercase'
                        }
                    ],
                    'validators': [{
                        'type': 'shiftcontent.validators.Required'
                    }]
                }]
            }]
        }

        service = DefinitionService()
        frozen = service.freeze_definition(data)
        self.assertIsInstance(frozen, frozendict)
        self.assertIsInstance(frozen['content'][0], frozendict)
        self.assertIsInstance(frozen['content'][0]['fields'][0], frozendict)
        self.assertIsInstance(
            frozen['content'][0]['fields'][0]['filters'][0], frozendict
        )
        self.assertIsInstance(
            frozen['content'][0]['fields'][0]['validators'][0], frozendict
        )

        with self.assertRaises(TypeError) as cm:
            frozen['content'][0]['fields'][0]['validators'][0]['type'] = 'crap'

        self.assertIn(
            "frozendict' object does not support item assignment",
            str(cm.exception)
        )

    def test_abort_if_detected_breaking_changes(self):
        """ Detect breaking changes in new revisions and abort """
        definition = {'content': [
            {
                'name': 'Markdown',
                'handle': 'markdown',
                'description': 'This is a markdown type',
                'editor': 'shiftcontent.editor.Editor',
                'fields': [
                    {
                        'name': 'Title',
                        'handle': 'title',
                        'description': 'Title copy',
                        'type': 'text',
                    },
                    {
                        'name': 'Body',
                        'handle': 'body',
                        'description': 'body text',
                        'type': 'text',
                    }
                ]
            },
            {
                'name': 'Plain Text',
                'handle': 'plain_text',
                'description': 'This is a markdown type',
                'editor': 'shiftcontent.editor.Editor',
                'fields': [
                    {
                        'name': 'Title',
                        'handle': 'title',
                        'description': 'Title copy',
                        'type': 'text',
                    },
                    {
                        'name': 'Body',
                        'handle': 'body',
                        'description': 'body text',
                        'type': 'text',
                    }
                ]
            },
        ]}

        service = DefinitionService()

        # ingest first revision
        valid1 = copy.deepcopy(definition)
        del valid1['content'][1]
        valid1_path = os.path.join(self.tmp, 'valid1.yml')
        with open(valid1_path, 'w') as stream:
            yaml.dump(valid1, stream)

        service.init(
            definition_path=valid1_path,
            revisions_path=self.revisions_path
        )
        service.definition
        time.sleep(1)

        # ingest second revision
        valid2 = copy.deepcopy(definition)
        valid2_path = os.path.join(self.tmp, 'valid2.yml')
        with open(valid2_path, 'w') as stream:
            yaml.dump(valid2, stream)

        service.init(
            definition_path=valid2_path,
            revisions_path=self.revisions_path
        )
        service.definition
        time.sleep(1)

        # ingest third revision (breaking changes!)
        valid3 = copy.deepcopy(definition)
        del valid3['content'][0]  # drop type
        del valid3['content'][0]['fields'][0] # drop field
        valid3['content'][0]['fields'][0]['type'] = 'boolean'  # change type

        valid3_path = os.path.join(self.tmp, 'valid3.yml')
        with open(valid3_path, 'w') as stream:
            yaml.dump(valid3, stream)

        service.init(
            definition_path=valid3_path,
            revisions_path=self.revisions_path
        )
        with self.assertRaises(x.BreakingSchemaChanges) as cm:
            pp(service.definition)

        err = cm.exception
        breaks = err.breaking_changes

        self.assertIn('missing_types', breaks)
        self.assertIn('Markdown', breaks['missing_types'][0])

        self.assertIn('missing_fields', breaks)
        self.assertIn('Plain Text: Title', breaks['missing_fields'][0])

        self.assertIn('field_type_changes', err.breaking_changes)
        self.assertIn('Plain Text: Body', breaks['field_type_changes'][0])











