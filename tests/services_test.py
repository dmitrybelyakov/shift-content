import unittest
from tests.base import BaseTestCase
from nose.plugins.attrib import attr


@attr('services')
class ServicesTest(BaseTestCase):
    """
    Services test
    This will check that services are actually importable
    and there are no circular import errors.
    """

    def test_importing_services(self):
        """ Importing globally accessible services """
        from shiftcontent.services import content
        import shiftcontent.content_service as cs
        self.assertIsInstance(content, cs.ContentService)

    def test_module_level_properties_instantiate_only_once(self):
        """ Instantiate services once only for module-level property access """
        from shiftcontent import services
        self.assertTrue(services.content is services.content)




