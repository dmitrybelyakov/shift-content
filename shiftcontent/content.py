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
from pprint import pprint as pp
from shiftcontent import exceptions as x


class ContentService:

    schema = None

    def __init__(self, schema_path):
        """
        Initialise service
        :param schema_path: str, yaml schema file path
        """
        self.schema = self.load_schema(schema_path)

    def load_schema(self, schema_path):
        """
        Load schema
        Loads a schema from a yaml file
        :param schema_path: str, yaml file path
        :return:
        """
        if not os.path.exists(schema_path):
            msg = 'Unable to locate schema file at path [{}]'
            raise x.ConfigurationException(msg.format(schema_path))
        with open(schema_path) as yml:
            yml = yaml.load(yml)
            schema = {t['handle'].lower(): t for t in yml['content']}

        return schema

    def process_schema(self, schema):
        """
        Process schema
        Performs schema syntax validation adn returns a nested dictionary of
        errors if schema is invalid.

        :param schema: dict, schema
        :return:
        """
        pass








    def create_item(self, type):
        pass

    def start_version(self, item_id):
        pass

    def commit_version(self, item_id, version_id):
        pass

    def set_field(self, field, value, version):
        pass






