import unittest
from nose.plugins.attrib import attr

import os
import shutil
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
    def known_path(self):
        """ Get path to known schemas """
        return os.path.join(
            os.getcwd(), 'var', 'data', 'tests', 'known_schemas'
        )

    def tearDown(self):
        """ Cleanup """
        super().tearDown()
        # if os.path.exists(self.known_path):
        #     shutil.rmtree(self.known_path)

    # --------------------------------------------------------------------------

    def test_create_content_service(self):
        """ Creating content service"""
        service = ContentService(self.schema_path, self.known_path)
        self.assertIsInstance(service, ContentService)

    def test_create_directory_for_known_schemas(self):
        """ Use known schemas property to create a directory"""
        path = self.known_path
        service = ContentService(
            schema_path=self.schema_path,
            known_path=path
        )

        self.assertFalse(os.path.exists(path))
        self.assertTrue(os.path.exists(service.known_schemas))

    def test_raise_when_unable_to_find_schema(self):
        """ Content service raises exception when unable to find schema file"""
        service = ContentService(
            schema_path=self.schema_path,
            known_path=self.known_path
        )
        with self.assertRaises(x.ConfigurationException):
            service.load_definition('/nothing/here')

    @attr('xxx')
    def test_persist_schema_if_does_not_exist(self):
        """ Persist new shemas for the first time"""
        service = ContentService(
            schema_path=self.schema_path,
            known_path=self.known_path
        )


        service.load_definition(self.schema_path)


