import click
from shiftcontent.cli.colours import *

# -----------------------------------------------------------------------------
# Group setup
# -----------------------------------------------------------------------------


@click.group(help=yellow('ShiftContent CLI'))
def cli():
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

from shiftcontent.cli.content import cli as content
cli.add_command(content, name='content')

from shiftcontent.cli.definition import cli as definition
cli.add_command(definition, name='definition')
