import os
import shutil
import yaml
import json
import hashlib
import arrow
from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent.schema import validator


class SchemaService:
    """
    Schema service
    Responsible for loading ant tracking schema fefinition file updates.
    """
    def __init__(self, schema_path, revisions_path):
        """
        Initialise service
        :param schema_path: str, yaml definition file path
        :param known_path: str, where to store known schemas
        """
        self.schema_path = schema_path
        self._revisions_path = revisions_path
        self._schema = None

    @property
    def revisions_path(self):
        """
        Revisions path
        Returns path to directory where we store schema revisions. Will check
        directory existence and create one if necessary .
        :return: str
        """
        path = self._revisions_path
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    @property
    def schema_revisions(self):
        """
        Schema revisions
        Returns a registry of revision hashes stored in a file under
        self.known_schemas. Backlog will have following structure:
           backlog = {
                '128762187612': {
                    'schema_file': '102981209821.yml',
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
    def schema(self):
        """
        Schema
        Returns current schema. If none is found will load from a definition.
        :return: dict
        """
        if not self._schema:
            self._schema = self.load_definition()
        return self._schema

    def register_revision(self, revision_filename):
        """
        Register revision
        Creates a record in revisions registry with a given filename.
        Will check revision file exisyence and abor if not found.
        :param revision_filename: str, schema filename
        :return: None
        """
        revision_file = os.path.join(self.revisions_path, revision_filename)
        if not os.path.isfile(revision_file):
            err = 'Error registering revision, revision file [{}] not found'
            raise x.UnableToRegisterSchemaRevision(err.format(revision_file))

        registry_file = os.path.join(self.revisions_path, '_registry.yml')
        registry_tmp = os.path.join(self.revisions_path, '_registry.yml.tmp')

        dt = arrow.utcnow()
        utc_timestamp = str(dt.timestamp)
        date = dt.format('YYYY-MM-DD HH:mm:ss')

        current_registry = self.schema_revisions
        current_registry[utc_timestamp] = dict(
            schema_file=revision_filename,
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
        if not os.path.exists(self.schema_path):
            msg = 'Unable to locate definition file at path [{}]'
            raise x.ConfigurationException(msg.format(self.schema_path))

        # load yaml
        with open(self.schema_path) as yml:
            text = yml.read()
            yml = yaml.load(text)
            schema = {t['handle'].lower(): t for t in yml['content']}

        # hash to see if changed
        hash = hashlib.md5(str(text).encode('utf-8')).hexdigest()
        revision_path = os.path.join(self.revisions_path, hash + '.yml')
        changed = not os.path.exists(revision_path)

        # return if not changed
        if not changed:
            return schema

        # if changed, validate and persist
        # todo: trigger schema changed event
        definitions_schema = validator.DefinitionSchema()
        ok = definitions_schema.process(yml)
        if not ok:
            errors = ok.get_messages()
            raise x.InvalidSchema(validation_errors=errors)
        else:
            schema = {t['handle'].lower(): t for t in yml['content']}

        # todo: check if fields were removed, field types changed etc

        # save schema to backlog
        shutil.copy(self.schema_path, revision_path)

        # save to revision registry
        self.register_revision(hash + '.yml')

        # todo: fire an event

        # and return
        return schema