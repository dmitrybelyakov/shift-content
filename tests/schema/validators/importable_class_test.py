from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.schema.validators import Importable


@attr('schema', 'validators', 'importable')
class ImportableTest(BaseTestCase):

    def test_instantiate_importable_class_validator(self):
        """ Instantiating importable class validator """
        validator = Importable()
        self.assertIsInstance(validator, Importable)

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
