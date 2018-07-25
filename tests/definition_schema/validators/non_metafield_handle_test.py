from tests.base import BaseTestCase
from nose.plugins.attrib import attr


from shiftcontent.definition_schema.validators import NonMetafieldHandle


@attr('schema', 'validators', 'non_metafield_handle')
class NonMetafieldHandleTest(BaseTestCase):

    def test_instantiate_handle_validator(self):
        """ Instantiating handle validator """
        validator = NonMetafieldHandle()
        self.assertIsInstance(validator, NonMetafieldHandle)

    def test_non_metafield_handle_passes_validation(self):
        """ Non-metafield field handles are allowed"""
        validator = NonMetafieldHandle()
        error = validator.validate('body')
        self.assertFalse(error)

    def test_metafield_handle_fails_validation(self):
        """ Metafield field handles are forbidden"""
        validator = NonMetafieldHandle()
        error = validator.validate('object_id')
        self.assertTrue(error)





