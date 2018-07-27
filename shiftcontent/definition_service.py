import os
import shutil
import yaml
import json
import hashlib
import arrow
from pprint import pprint as pp
from frozendict import frozendict
from shiftcontent import exceptions as x


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

    def load_definition(self):
        """
        Load definition
        Loads a definition from a yaml file
        :return: dict
        """
        from shiftcontent.definition_schema import schema

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
        definitions_schema = schema.DefinitionSchema()
        ok = definitions_schema.process(yml)
        if not ok:
            errors = ok.get_messages()
            raise x.InvalidDefinition(validation_errors=errors)
        else:
            definition = {t['handle'].lower(): t for t in yml['content']}

        # todo: trigger schema changed event
        # todo: check if fields were removed, field types changed etc

        # save definition to backlog
        shutil.copy(self.definition_path, revision_path)

        # save to revision registry
        self.register_revision(hash + '.yml')

        # todo: fire an event

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



