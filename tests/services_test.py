from tests.base import BaseTestCase
from nose.plugins.attrib import attr
import shiftschema
import shiftschema.schema
from shiftschema.schema import Schema

from shiftcontent.utils import import_by_name


@attr('services')
class ServicesTest(BaseTestCase):

    def test_importing_from_globals(self):
        """ Importing from globals """
        from shiftcontent import services
        print(globals)
        import pdb; pdb.set_trace();


