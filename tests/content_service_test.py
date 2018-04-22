import unittest
from nose.plugins.attrib import attr

import os
import shutil
import hashlib
import yaml
import json
from pprint import pprint as pp
from shiftcontent.content import ContentService
from shiftcontent import exceptions as x


@attr('content')
class ContentServiceTest(unittest.TestCase):

    @property
    def schema_path(self):
        """ Get path to content schema file """
        path = os.path.join(os.getcwd(), 'shiftcontent', 'content.yml')
        return path

    @property
    def revisions_path(self):
        """ Get path to schema revisions """
        return os.path.join(
            os.getcwd(), 'var', 'data', 'tests', 'known_schemas'
        )

    @property
    def tmp(self):
        """ Get path to temp data """
        tmp = os.path.join(
            os.getcwd(), 'var', 'data', 'tests', 'tmp'
        )
        if not os.path.exists(tmp):
            os.makedirs(tmp, exist_ok=True)
        return tmp

    def create_tmp(self):
        """ Creates tenmp directory"""
        if not os.path.exists(self.tmp):
            os.makedirs(self.tmp, exist_ok=True)
        return self.tmp

    def tearDown(self):
        """ Cleanup """
        super().tearDown()
        tests = os.path.join(os.getcwd(), 'var', 'data', 'tests')
        if os.path.exists(tests): shutil.rmtree(tests)

    # --------------------------------------------------------------------------

    def test_create_content_service(self):
        """ Creating content service"""
        service = ContentService(self.schema_path, self.revisions_path)
        self.assertIsInstance(service, ContentService)

    def test_create_revisions_directory_on_first_access(self):
        """ Create directory for schema revisions if does not exist """
        path = self.revisions_path
        service = ContentService(
            schema_path=self.schema_path,
            revisions_path=path
        )

        self.assertFalse(os.path.exists(path))
        self.assertTrue(os.path.exists(service.revisions_path))

    def test_registry_is_empty_if_no_file(self):
        """ Return empty dict if registry file does not exist"""
        service = ContentService(
            schema_path=self.schema_path,
            revisions_path=self.revisions_path
        )

        registry = service.schema_revisions
        self.assertTrue(type(registry) is dict)
        self.assertFalse(registry)

    def test_load_parse_and_return_existing_registry(self):
        """ Existing regitry can be loaded successfully into a dict"""
        service = ContentService(
            schema_path=self.schema_path,
            revisions_path=self.revisions_path
        )

        registry = {
            '91827219871298': {
                'schema_file': '102981209821.yml',
                'date': '2016-04-22 12:45:00'
            }
        }

        registry_json = json.dumps(registry, ensure_ascii=False, indent=4)
        registry_file = os.path.join(service.revisions_path, '_registry.yml')
        with open(registry_file, 'w') as file:
            file.write(registry_json)

        loaded_registry = service.schema_revisions
        self.assertEquals(registry, loaded_registry)

    def test_raise_when_unable_to_find_schema(self):
        """ Content service raises exception when unable to find schema file"""
        service = ContentService(
            schema_path='/nothing/here',
            revisions_path=self.revisions_path
        )
        with self.assertRaises(x.ConfigurationException):
            service.load_definition()

    def test_raise_when_definition_fails_validation(self):
        """ Raise exception when schema fails validation"""
        invalid = {'content': [
            {
                'name': 'Markdown',
                'handle': 'markdown',
                'editor': 'shiftcontent.editor.Default',
                'fields': []
            },
        ]}

        tmp = self.create_tmp()
        path = os.path.join(tmp, 'invalid.yml')
        with open(path, 'w') as stream:
            yaml.dump(invalid, stream)

        service = ContentService(
            schema_path=path,
            revisions_path=self.revisions_path
        )

        with self.assertRaises(x.InvalidSchema):
            service.load_definition()

    def test_ingest_valid_schema(self):
        """ Save schema file to schema revisions backlog """
        valid = {'content': [
            {
                'name': 'Markdown',
                'handle': 'markdown',
                'description': 'This is a markdown type',
                'editor': 'shiftcontent.editor.Default',
                'fields': []
            },
        ]}

        tmp = self.create_tmp()
        path = os.path.join(tmp, 'valid.yml')
        with open(path, 'w') as stream:
            yaml.dump(valid, stream)

        service = ContentService(
            schema_path=path,
            revisions_path=self.revisions_path
        )

        service.load_definition()
        with open(path) as yml:
            text = yml.read()

        # assert saved to backlog
        hash = hashlib.md5(str(text).encode('utf-8')).hexdigest()
        target = os.path.join(self.revisions_path, hash + '.yml')
        self.assertTrue(os.path.isfile(target))

        # assert saved to registry
        registry = service.schema_revisions
        self.assertEquals(
            hash + '.yml',
            registry[list(registry.keys())[0]]['schema_file']
        )

    def test_abort_schema_revision_registering_if_no_file(self):
        """ Abord adding revision to registry if file not found"""
        service = ContentService(
            schema_path=self.schema_path,
            revisions_path=self.revisions_path
        )

        with self.assertRaises(x.UnableToRegisterSchemaRevision):
            service.register_revision('nothing.yml')

    def test_can_register_schema_revision(self):
        """ Resgistering schema revision"""
        service = ContentService(
            schema_path=self.schema_path,
            revisions_path=self.revisions_path
        )

        path = service.revisions_path
        revision_file = os.path.join(path, 'randomhash.yml')
        with open(revision_file, 'w') as revision:
            revision.writelines(['revision yaml data'])

        service.register_revision('randomhash.yml')
        registry = service.schema_revisions
        self.assertTrue(type(registry) is dict)
        self.assertEquals(1, len(registry.keys()))
        self.assertEquals(
            'randomhash.yml',
            registry[list(registry.keys())[0]]['schema_file']
        )




