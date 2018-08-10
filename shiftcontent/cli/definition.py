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

    def print_type(index, data):
        """ Print content type errors"""
        print(green('Content type "{}": '.format(index)))

        for field, errors in data.items():

            if type(errors) is list:
                for type_field_err in errors:
                    print('{} - {}'.format(' ' * 4, type_field_err))

            if type(errors) is dict:
                print(yellow('{} * {}:'.format(' ' * 4, field)))
                if 'direct' in errors:
                    for type_field_err in errors['direct']:
                        print('{} - {}'.format(' ' * 8, type_field_err))

                if 'collection' in errors:
                    fields = errors['collection']
                    for field_index, field_errors in fields.items():
                        print_field(field_index, field_errors)

    def print_field(index, data):
        """ Print field errors"""
        print(green('{} * Field "{}":'.format(' ' * 8, index)))

        for field, errors in data.items():
            if type(errors) is list:
                for field_err in errors:
                    print('{} - {}'.format(' ' * 16, field_err))

            if type(errors) is dict:
                print(yellow('{} * {}: '.format(' ' * 16, field)))

                if type(errors) is dict and 'direct' in errors:
                    for type_field_err in errors['direct']:
                        print('{} - {}'.format(' ' * 20, type_field_err))

                if 'collection' in errors:
                    processors = errors['collection']
                    for field_index, field_errors in processors.items():
                        print_filer_or_validator(
                            field_index,
                            field_errors,
                            'Filter' if field == 'filters' else 'Validator'
                        )

    def print_filer_or_validator(index, data, object_type=None):
        """ Print filter/validator errors"""
        if not object_type:
            object_type = 'Filter/Validator'

        print(green('{} * {} "{}":'.format(' ' * 20, object_type, index)))
        for prop, errors in data.items():
            for error in errors:
                print('{} - {}'.format(' ' * 24, error))

    errors = ok.get_messages()
    
    content = errors['content']
    if 'direct' in content:
        print(red('Content types:'))
        for err in content['direct']:
            print('{} * {}'.format(' ' * 4, err))
        print()

    # got types?
    if 'collection' not in content:
        print()
        return

    types = content['collection']
    for index, content_type in types.items():
        print_type(index, content_type)
        print()



    # done
    return


@cli.command(name='load')
@click.argument('path')
@click.option('--force', default=False)
def load_definition(path, force=False):
    """ Ingest new verion of content definition """
    print(yellow('Validating definition file'))
    print(green('path: {}'.format(path)))
    print(yellow('-' * 80))

