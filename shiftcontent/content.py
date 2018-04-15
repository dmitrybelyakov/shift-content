class Page:
    meta = None
    modules = []


class ContentType:
    """
    Module
    """
    type = None
    name = None
    description = None
    screenshot = None
    fields = {
        'Body': 'text'
    }

    def __init__(self, definition):
        """
        Initializes content item
        :param definition: dict, configuration
        :param store: state store
        """
        pass

    def get_new_item(self):
        """
        Get new item
        Factory method to create an item of this type
        :return:
        """
        pass


class ContentItem:
    id = None
    type = None
    version = None
    fields = None

    def __init__(self, data):
        pass

    def to_dict(self):
        return dict()


import os
import shutil
import yaml
import hashlib
from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import schema as schemas


class ContentService:

    def __init__(self, schema_path, known_path):
        """
        Initialise service
        :param schema_path: str, yaml definition file path
        :param known_path: str, where to store known schemas
        """
        self.schema_path = schema_path
        self._known_schemas_path = known_path
        self._schema = None

    @property
    def known_schemas(self):
        """
        Known schemas
        Returns path to known schemas. Will check directory existence and
        create one if necessary .
        :return: str
        """
        path = self._known_schemas_path
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    @property
    def schema(self):
        """
        Schema
        Returns current schema. If none is found will load from a definition.
        :return: dict
        """
        if not self._schema:
            self._schema = self.load_definition(self.schema_path)
        return self._schema

    def load_definition(self, schema_path):
        """
        Load definition
        Loads a definition from a yaml file
        :param schema_path: str, yaml file path
        :return: dict
        """
        if not os.path.exists(schema_path):
            msg = 'Unable to locate definition file at path [{}]'
            raise x.ConfigurationException(msg.format(schema_path))

        # read current schema
        with open(schema_path) as yml:
            text = yml.read()

        # hash definition and see if changed
        hash = hashlib.md5(str(text).encode('utf-8')).hexdigest()
        known_schema = os.path.join(self.known_schemas, hash + '.yml')
        changed = not os.path.exists(known_schema)

        # todo: how to go back in history with schema changes?
        # todo: how to identify which schema was previous?
        # todo: how do we handle field deletions?

        # if changed, validate and save
        if changed:
            shutil.copy(schema_path, known_schema)

        # and return
        yml = yaml.load(text)
        schema = {t['handle'].lower(): t for t in yml['content']}
        return schema

    def update_schema(self, new_schema):
        """
        Update schema
        Validates new schema, then checks if content types or fields were
        removed which can result in data loss. If the latter discovered will
        raise an error, unless forced. In force mode will remove all data
        from the database that is missing from the schema. Finally persists
        schema definition as a new schema.

        :param new_schema: dict, schema
        :return:
        """
        # todo: do we actually delete data from the database?
        # todo: or simply don't show it?
        # todo: if we do, what happens to events in store that have the fields?

        # todo: how to address gdpr?
        # todo: https://www.michielrook.nl/2017/11/forget-me-please-event-sourcing-gdpr/
        # todo: https://www.michielrook.nl/2017/11/event-sourcing-gdpr-follow-up/
        # todo: 1. we can and must edit events in store
        # todo: 2. events must be associated with a user
        # todo: 3. all such events will be obfuscated (possibly removed)

        # todo: validate new schema here
        # todo: load old schema and check if fields deleted



        pass


    def process_definition(self, definition):
        """
        Process definition
        Performs definition syntax validation adn returns a nested dictionary of
        errors if definitiuon is invalid.

        :param definition: dict, definition
        :return:
        """
        errors = []

        for content_type in definition.items():
            schema = schemas.DefinitionSchema()
            valid = schema.process(content_type)

            for field in content_type['fields']:
                field_schema = schemas.FieldSchema()
                field_valid = field_schema.valid









    def create_item(self, type):
        pass

    def start_version(self, item_id):
        pass

    def commit_version(self, item_id, version_id):
        pass

    def set_field(self, field, value, version):
        pass






