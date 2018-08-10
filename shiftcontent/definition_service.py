import os
import shutil
import yaml
import json
import hashlib
import arrow
import time
from pprint import pprint as pp
from frozendict import frozendict
from shiftcontent import exceptions as x
from shiftcontent.definition_schema.schema import DefinitionSchema


class DefinitionService:
    """
    Content definition service
    Responsible for loading ant tracking definition file updates.
    """
    def __init__(self, *args, **kwargs):
        """
        Init service
        If any parameters are given to constructor, a delayed initializer is
        called with these parameters.
        """
        self.definition_path = None
        self._revisions_path = None
        self._definition = None

        if args or kwargs:
            self.init(*args, **kwargs)

    def init(self, definition_path, revisions_path):
        """
        Delayed service initializer
        :param definition_path: str, yaml definition file path
        :param revisions_path: str, where to store definition revisions
        """
        self.definition_path = definition_path
        self._revisions_path = revisions_path
        self._definition = None
        return self

    @property
    def revisions_path(self):
        """
        Revisions path
        Returns path to directory where we store definition revisions.
        Will check directory existence and create one if necessary .
        :return: str
        """
        path = self._revisions_path
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    @property
    def revisions(self):
        """
        Definition revisions
        Returns a registry of revision hashes stored in a file under
        self.revisions_path. Backlog will have following structure:
           backlog = {
                '128762187612': {
                    'revision_file': '102981209821.yml',
                    'date': 'YYYY-MM-DD HH:mm:ss'
                }
            }

        :return: dict
        """
        registry = os.path.join(self.revisions_path, '_registry.yml')
        if not os.path.exists(registry):
            return dict()

        with open(registry) as file:
            text = file.read()

        text = json.loads(text)
        return text

    @property
    def definition(self):
        """
        Definition
        Returns current definition. If none is found will load it from
        definition file.
        :return: dict
        """
        if not self._definition:
            self._definition = self.load_definition()
        return self._definition

    def get_type(self, content_type):
        """
        Get type definition
        Finds content type definition by it's handle and returns that. May
        raise an error if requesting definition for nonexistent type.

        :param content_type: str, content type handle
        :return: dict
        """
        if content_type not in self.definition:
            msg = 'Unable to find definition for content type [{}]'
            raise x.UndefinedContentType(msg.format(content_type))

        # otherwise return
        return self.definition[content_type]

    def validate_definition(self, definition):
        """
        Validate definition
        Applies filres and validators to incoming definition dict and returns
        a validation result object (with errors or empty)
        :param definition: dict, definition to validate
        :return: shiftschema.result.Result
        """
        schema = DefinitionSchema()
        result = schema.process(definition)
        return result

    def register_revision(self, revision_filename):
        """
        Register revision
        Creates a record in revisions registry with a given filename.
        Will check revision file existence and abort if not found.
        :param revision_filename: str, definition filename
        :return: None
        """
        revision_file = os.path.join(self.revisions_path, revision_filename)
        if not os.path.isfile(revision_file):
            err = 'Error registering revision, revision file [{}] not found'
            raise x.UnableToRegisterRevision(err.format(revision_file))

        registry_file = os.path.join(self.revisions_path, '_registry.yml')
        registry_tmp = os.path.join(self.revisions_path, '_registry.yml.tmp')

        dt = arrow.utcnow()
        utc_timestamp = str(dt.timestamp)
        date = dt.format('YYYY-MM-DD HH:mm:ss')

        current_registry = self.revisions
        current_registry[utc_timestamp] = dict(
            definition_file=revision_filename,
            date=date
        )

        new_registry = dict()
        for timestamp in sorted(current_registry.keys()):
            new_registry[timestamp] = current_registry[timestamp]

        registry_json = json.dumps(new_registry, ensure_ascii=False, indent=4)
        with open(registry_tmp, 'w') as file:
            file.write(registry_json)

        shutil.copy(registry_tmp, registry_file)
        os.remove(registry_tmp)

    def load_definition(self, force=False):
        """
        Load definition
        Loads a definition from a yaml file. Will check if changed since
        previous version and if so validate and persist. Additionally checks
        if new revision introduced breaking changes, i.g. deleted fields or
        changed field types and aborts persistence with an exception, unless
        force flag is set to True

        :param force: bool, whether to force-load on breaking changes
        :return: dict
        """
        if not os.path.exists(self.definition_path):
            msg = 'Unable to locate definition file at path [{}]'
            raise x.ConfigurationException(msg.format(self.definition_path))

        # load yaml
        with open(self.definition_path) as yml:
            text = yml.read()
            yml = yaml.load(text)
            definition = {t['handle'].lower(): t for t in yml['content']}

        # hash to see if changed
        hash = hashlib.md5(str(text).encode('utf-8')).hexdigest()
        revision_path = os.path.join(self.revisions_path, hash + '.yml')
        changed = not os.path.exists(revision_path)

        # return if not changed
        if not changed:
            return self.freeze_definition(definition)

        # if changed, validate and persist
        ok = self.validate_definition(yml)
        if not ok:
            errors = ok.get_messages()
            raise x.InvalidDefinition(validation_errors=errors)
        else:
            definition = {t['handle'].lower(): t for t in yml['content']}

        # check for breaking changes
        if self.revisions:
            max_index = max((key for key in self.revisions.keys()))
            latest = self.revisions.get(str(max_index))['definition_file']
            latest_path = os.path.join(self.revisions_path, latest)
            with open(latest_path) as prev:
                prev = yaml.load(prev.read())
                content = prev['content']
                previous_revision = {t['handle'].lower(): t for t in content}
                self.detect_breaking_changes(
                    old_version=previous_revision,
                    new_version=definition
                )

        # save definition to backlog
        shutil.copy(self.definition_path, revision_path)

        # save to revision registry
        self.register_revision(hash + '.yml')

        # and return
        return self.freeze_definition(definition)

    def freeze_definition(self, definition):
        """
        Freeze definition
        Recursively freezes definition to prevent accidental in-place
        modifications.

        :param definition:
        :return:
        """
        fd = self.freeze_definition

        branch = dict()
        for prop, val in definition.items():
            if type(val) is dict:
                branch[prop] = fd(val)
                continue

            elif type(val) is list:
                lst = [fd(v) if type(v) is dict else v for v in val]
                branch[prop] = lst
                continue

            else:
                branch[prop] = val

        # freeze and return
        return frozendict(branch)

    def detect_breaking_changes(self, old_version, new_version):
        """
        Detect breaking changes
        Accepts to definitions to compare new_version against old_version for
        breaking changes, e.g. field deletions or field type changes.

        :param old_version: dict, old (current) definition
        :param new_version: dict, new definition to be applied
        :return: shiftcontent.definition_service.DefinitionService
        """

        # errors
        errors = dict(
            missing_types=[],
            missing_fields=[],
            field_type_changes=[]
        )

        for content_type, type_def in old_version.items():
            # check for content type deletions
            if content_type not in new_version:
                errors['missing_types'].append(type_def['name'])
                continue

            for field in type_def['fields']:
                found = list(filter(
                    lambda x: x['handle'] == field['handle'],
                    new_version[content_type]['fields']
                ))

                # check for missing fields
                if not found:
                    errors['missing_fields'].append('{}: {}'.format(
                        type_def['name'],
                        field['name']
                    ))
                    continue

                # check for field type changes
                found = found[0]
                if field['type'] != found['type']:
                    err = '{}: {} ({} -> {})'
                    errors['field_type_changes'].append(err.format(
                        type_def['name'],
                        field['name'],
                        field['type'],
                        found['type']
                    ))
                    continue

        has_errors = False
        for key in errors.keys():
            if errors[key]:
                has_errors = True

        # return on success
        if not has_errors:
            return self

        # otherwise raise exception
        err = 'Unable to load new definition: breaking changes detected:\n'
        for key in errors.keys():
            if not errors[key]:
                continue

            if key == 'missing_types':
                err += 'Content types deleted: {}\n'.format(
                    ' '.join(errors[key])
                )
            if key == 'missing_fields':
                err += 'Fields deleted: {}\n'.format(
                    ' '.join(errors[key])
                )
            if key == 'field_type_changes':
                err += 'Fields types changed: {}\n'.format(
                    ', '.join(errors[key])
                )

        # raise
        raise x.BreakingSchemaChanges(err, breaking_changes=errors)





