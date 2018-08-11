from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from click.testing import CliRunner
from shiftcontent.cli import cli


@attr('cli')
class CliTest(BaseTestCase):
    """
    CLI tests
    For testing CLI commands see: http://click.pocoo.org/5/testing/
    """

    def test_run_cli(self):
        """ Running content cli """
        runner = CliRunner()
        result = runner.invoke(cli)
        self.assertEquals(0, result.exit_code)
        self.assertIn('definition  Definition commands', result.output)





