import click, os, sys, shutil
from shiftcontent.cli.colours import *
import yaml
import os
from pprint import pprint as pp
from boiler.cli import get_app
from shiftcontent import definition_service
import time

# -----------------------------------------------------------------------------
# Group setup
# -----------------------------------------------------------------------------


@click.group(help=yellow('Definition commands'))
def cli():
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

@cli.command(name='validate')
@click.argument('path')
def validate_definition(path):
    """ Validate content definition """
    print(yellow('\nValidating definition file: {}'.format(path)))
    print(yellow('-' * 80))

    if not os.path.isfile(path):
        print(red('Definition file does not exist\n'))
        return

    yml = None
    try:
        with open(path) as file:
            text = file.read()
            yml = yaml.load(text)
    except UnicodeDecodeError:
        pass

    if not yml:
        print(red('Invalid definition YAML\n'))
        return

    # validate
    ok = definition_service.validate_definition(yml)
    if ok:
        print(green('Definition file is valid!\n'))
        return

    print(red('DEFINITION INVALID:\n'))
    errors = ok.get_messages()

    # pp(errors)

    # content
    if 'content' in errors and 'direct' in errors['content']:
        print(green('Content (root element): \n'))
        for direct in errors['content']['direct']:
            print(red(direct + '\n'))

    types = errors['content']['collection']
    pp(types)

    for index, type_errors in types.items():
        print(green('Content type #{}: \n'.format(index)))
        for field, field_errors in type_errors.items():
            print(yellow('{}:'.format(field)))

            if type(field_errors) is list:
                for field_error in field_errors:
                    print('{} * {} \n'.format(' ' * 4, field_error))

            if type(field_errors) is dict and 'direct' in field_errors:
                for field_error in field_errors['direct']:
                    print('{} * {} \n'.format(' ' * 4, field_error))

            if type(field_errors) is dict and 'collection' in field_errors:
                collection_errors = field_errors['collection']
                for subfield, subfield_errors in collection_errors.items():
                    print(magenta('{} * Field {}:\n'.format(' ' * 4, subfield)))

                    print(subfield_errors)

                    # if type(subfield_errors) is list:
                    #     for subfield_error in subfield_errors:
                    #         print('{} * {}'.format(tab, subfield_error))





        # print()










@cli.command(name='load')
@click.argument('path')
@click.option('--force', default=False)
def load_definition(path, force=False):
    """ Ingest new verion of content definition """
    print(yellow('Validating definition file'))
    print(green('path: {}'.format(path)))
    print(yellow('-' * 80))

