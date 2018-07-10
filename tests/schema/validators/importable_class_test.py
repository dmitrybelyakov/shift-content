from tests.base import BaseTestCase
from nose.plugins.attrib import attr
import shiftschema
import shiftschema.schema
from shiftschema.schema import Schema

from shiftcontent.schema.validators import Importable


@attr('schema', 'validators', 'importable')
class ImportableTest(BaseTestCase):

    def test_instantiate_importable_class_validator(self):
        """ Instantiating importable class validator """
        validator = Importable()
        self.assertIsInstance(validator, Importable)

    def test_importing_module(self):
        """ Importing module by name """
        validator = Importable()
        name = 'shiftschema'
        imported = validator.import_by_name(name)
        self.assertEquals(imported, shiftschema)

    def test_import_submodule_by_name(self):
        """ Import submodule by name """
        validator = Importable()
        name = 'shiftschema.schema'
        imported = validator.import_by_name(name)
        self.assertEquals(imported, shiftschema.schema)

    def test_import_module_attribute(self):
        """ Importing module attribute """
        validator = Importable()
        name = 'shiftschema.schema.Schema'
        imported = validator.import_by_name(name)
        self.assertEquals(imported, Schema)

    def test_importable_class_passes_validation(self):
        """ Importable class passes validation """
        validator = Importable()
        cls = 'shiftschema.schema.Schema'
        error = validator.validate(cls)
        self.assertFalse(error)

    def test_nonimportable_class_fails_validation(self):
        """ Non-importable class fails validation """
        validator = Importable()
        error = validator.validate('shiftschema.schema.Schemaz')
        self.assertTrue(error)
