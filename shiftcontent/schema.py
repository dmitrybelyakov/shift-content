from shiftschema.schema import Schema
from shiftschema import validators as validator
from shiftschema import filters as filter


class DefinitionSchema(Schema):
    """
    Content definition schema
    Used to validate content type definitions
    """
    def schema(self):

        # content type name
        self.add_property('name', required=True)
        self.name.add_filter(filter.Strip())

        # content type handle
        self.add_property('handle', required=True)
        self.handle.add_filter(filter.Strip())
        self.handle.add_filter(filter.Lowercase())

        # content type description
        self.add_property('description')
        self.description.add_filter(filter.Strip())

        # content type preview url
        self.add_property('preview')
        self.preview.add_filter(filter.Strip())

        # content type editor
        self.add_property('editor', required=True)
        self.editor.add_filter(filter.Strip())


class FieldSchema(Schema):
    """
    Content field definition schema
    Used to validate field definitions attached to content type
    """
    def schema(self):

        # field name
        self.add_property('name', required=True)
        self.name.add_filter(filter.Strip())

        # field handle
        self.add_property('handle', required=True)
        self.handle.add_filter(filter.Strip())
        self.handle.add_filter(filter.Lowercase())

        # field description
        self.add_property('description')
        self.description.add_filter(filter.Strip())

        # field type
        self.add_property('type')
        self.type.add_filter(filter.Strip())
        self.type.add_filter(filter.Lowercase())
        self.type.add_validator(validator.Choice(['text']))

        # field default value
        self.add_property('default_value')
        self.type.add_filter(filter.NoneString())


