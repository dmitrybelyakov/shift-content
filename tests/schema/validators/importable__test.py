from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.schema.validators import Instantiatable


@attr('schema', 'validators', 'instantiatable')
class ImportableTest(BaseTestCase):

    def test_instantiate_instantiatable_class_validator(self):
        """ Instantiating instantiatable class validator """
        validator = Instantiatable()
        self.assertIsInstance(validator, Instantiatable)

    def test_instantiatable_class_passes_validation(self):
        """ Instantiatable class passes validation """
        validator = Instantiatable()
        cls = 'shiftschema.validators.Length'
        model = dict(
            type=cls,
            min=10,
            max=20
        )

        error = validator.validate(cls, model=model)
        self.assertFalse(error)

    def test_non_instantiatable_class_fails_validation(self):
        """ Non-importable class fails validation """
        validator = Instantiatable()
        cls = 'shiftschema.validators.Length'
        model = dict(
            type=cls,
            bad='stuff'
        )
        error = validator.validate(cls, model=model)
        self.assertTrue(error)
