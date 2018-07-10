from tests.base import BaseTestCase
from nose.plugins.attrib import attr
import shiftschema
import shiftschema.schema
from shiftschema.schema import Schema

from shiftcontent.schema.validators import ImportableClass

test = 'a string'

@attr('schema', 'validators', 'importable_class')
class ImportableClassTest(BaseTestCase):

    def test_instantiate_importable_class_validator(self):
        """ Instantiating importable class validator """
        validator = ImportableClass()
        self.assertIsInstance(validator, ImportableClass)

    def test_importing_module(self):
        """ Importing module by name """
        validator = ImportableClass()
        name = 'shiftschema'
        imported = validator.import_by_name(name)
        self.assertEquals(imported, shiftschema)

    def test_import_submodule_by_name(self):
        """ Import submodule by name """
        validator = ImportableClass()
        name = 'shiftschema.schema'
        imported = validator.import_by_name(name)
        self.assertEquals(imported, shiftschema.schema)

    def test_import_module_attribute(self):
        """ Importing module attribute """
        validator = ImportableClass()
        name = 'shiftschema.schema.Schema'
        imported = validator.import_by_name(name)
        self.assertEquals(imported, Schema)

    def test_importable_class_passes_validation(self):
        """ Importable class passes validation """
        validator = ImportableClass()
        cls = 'shiftschema.schema.Schema'
        error = validator.validate(cls)
        self.assertFalse(error)


    @attr('zzzz')
    def Test_nonimportable_class_fails_validation(self):
        """ Non-importable class fails validation """
        validator = ImportableClass()
        error = validator.validate('noneexistent.thing')
        self.assertTrue(error)

