import click, os, sys, shutil
from shiftcontent.cli.colours import *
import yaml
import os
from pprint import pprint as pp
from shiftcontent import definition_service
from shiftcontent import exceptions as x

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
            definition = {t['handle'].lower(): t for t in yml['content']}
    except UnicodeDecodeError:
        pass

    if not yml:
        print(red('Invalid definition YAML\n'))
        return

    # validate
    ok = definition_service.validate_definition(yml)
    if ok:
        print(green('Definition file is valid!\n\n'))
        print(yellow('Checking for breaking changes:'))
        print(yellow('-' * 80))

        previous_revision = definition_service.get_latest_revision()

        try:
            definition_service.detect_breaking_changes(
                old_version=previous_revision,
                new_version=definition
            )
        except x.BreakingSchemaChanges as err:

            print('Breaking changes detected. That may result in data loss.')
            print('Be careful and consider the changes you are making.')
            print('If you know what you are doing, use the force-load command')
            print('to apply those changes.\n')

            changes = err.breaking_changes
            if 'missing_types' in changes and changes['missing_types']:
                print(red('Content types deleted:'))
                for content in changes['missing_types']:
                    print('{} * {}'.format(' ' * 4, content))
                print()

            if 'missing_fields' in changes and changes['missing_fields']:
                print(red('Content fields deleted:'))
                for field in changes['missing_fields']:
                    print('{} * {}'.format(' ' * 4, field))
                print()

            if 'field_type_changes' in changes and changes['field_type_changes']:
                print(red('Content fields types changed:'))
                for field_type in changes['field_type_changes']:
                    print('{} * {}'.format(' ' * 4, field_type))
                print()


            # pp(changes)
            return

        # success otherwise
        print(green('No breaking changes detected\n'))


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
    if 'direct' in errors['content']:
        print(red('Content types:'))
        for err in errors['content']['direct']:
            print('{} * {}'.format(' ' * 4, err))
        print()

    # got types?
    if 'collection' not in errors['content']:
        print()
        return

    types = errors['content']['collection']
    for index, content_type in types.items():
        print_type(index, content_type)
        print()

    # done
    return


@cli.command(name='force-load')
def force_load_definition():
    """ Force loading of definition with breaking changes """
    from shiftcontent import definition_service
    print(definition_service.definition_path)
    print(definition_service.revisions)

