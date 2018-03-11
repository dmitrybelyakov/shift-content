import unittest
from nose.plugins.attrib import attr

import os
from pprint import pprint as pp
from shiftcontent.content import ContentService
from shiftcontent import exceptions as x


@attr('content')
class ContentServiceTest(unittest.TestCase):

    def shchema_path(self):
        """ Get path to content schema file """
        path = os.path.join(os.getcwd(), 'shiftcontent', 'content.yml')
        return path

    # --------------------------------------------------------------------------

    def test_create_content_service(self):
        """ Creating content service"""
        service = ContentService(self.shchema_path())
        self.assertIsInstance(service, ContentService)

    def test_raise_when_unable_to_find_schema(self):
        """ Content service raises exception when unable to find schema file"""
        with self.assertRaises(x.ConfigurationException):
            ContentService('bullshit')

    @attr('zzz')
    def test_loading_yaml_schema_on_instantiation(self):
        """ Content service loads yaml schema on instantiation"""
        service = ContentService(self.shchema_path())
        self.assertIsNotNone(service.schema)
        pp(service.schema)


    def can_create_item_of_type(self):
        """ Can create content item """
        pass

