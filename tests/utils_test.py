from tests.base import BaseTestCase
from nose.plugins.attrib import attr
import shiftschema
import shiftschema.schema
from shiftschema.schema import Schema
from pprint import pprint as pp
from shiftcontent.utils import import_by_name


@attr('utils')
class UtilsTest(BaseTestCase):

    def test_importing_module(self):
        """ Importing module by name """
        name = 'shiftschema'
        imported = import_by_name(name)
        self.assertEquals(imported, shiftschema)

    def test_import_submodule_by_name(self):
        """ Import submodule by name """
        name = 'shiftschema.schema'
        imported = import_by_name(name)
        self.assertEquals(imported, shiftschema.schema)

    def test_import_module_attribute(self):
        """ Importing module attribute """
        name = 'shiftschema.schema.Schema'
        imported = import_by_name(name)
        self.assertEquals(imported, Schema)
