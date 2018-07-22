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




