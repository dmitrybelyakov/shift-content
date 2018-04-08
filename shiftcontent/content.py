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
    id: None
    type: ContentType
    version: None
    fields: []

    def __init__(self, data):
        pass

    def to_dict(self):
        return dict()


import os
import yaml
import hashlib
from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent import schema as schemas


class ContentService:

    def __init__(self, schema_path: str, known_path: str) -> None:
        """
        Initialise service
        :param schema_path: str, yaml definition file path
        :param known_path: str, where to store known schemas
        """
        self.schema_path: str = schema_path
        self._known_schemas_path: str = known_path
        self._schema: dict = None

    @property
    def known_schemas(self) -> str:
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
    def schema(self) -> dict:
        """
        Schema
        Returns current schema. If none is found will load from a definition.
        :return: dict
        """
        if not self._schema:
            self._schema = self.load_definition(self.schema_path)
        return self._schema

    def load_definition(self, schema_path) -> dict:
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


        hash = hashlib.md5(str(text).encode('utf-8')).hexdigest()
        # known_schema = os.path.join(self.known_schemas, hash + '.yml')

        # print(known_schema)



        yml = yaml.load(text)
        schema = {t['handle'].lower(): t for t in yml['content']}



        return schema

    def process_definition(self, definition: dict) -> None:
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






