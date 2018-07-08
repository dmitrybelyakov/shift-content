from shiftschema.schema import Schema
from shiftschema import validators as validator
from shiftschema import filters as filter

from shiftcontent.schema import validators as content_validators

class TypeSchema(Schema):
    """
    Type schema
    Used to validate content types. This will be applied to every content type
    in the collection.
    """
    def schema(self):
        # content type name
        self.add_property('name')
        self.name.add_filter(filter.Strip())
        self.name.add_validator(validator.Required())
        self.name.add_validator(content_validators.UniqueTypeName())

        # content type handle
        self.add_property('handle')
        self.handle.add_filter(filter.Strip())
        self.handle.add_filter(filter.Lowercase())
        self.handle.add_validator(validator.Required())
        self.handle.add_validator(content_validators.UniqueTypeHandle())

        # content type description
        self.add_property('description')
        self.description.add_filter(filter.Strip())
        self.description.add_validator(validator.Required())

        # content type preview url
        self.add_property('preview')
        self.preview.add_filter(filter.Strip())
        # todo: url must be valid

        # content type editor
        self.add_property('editor')
        self.editor.add_filter(filter.Strip())
        self.editor.add_validator(validator.Required())
        # todo: editor must be importable


class DefinitionSchema(Schema):
    """
    Content definition schema
    Used to validate content type definitions
    """
    def schema(self):
        self.add_collection('content')
        # self.content.add_validator(content_validators.UniqueTypeName())
        self.content.schema = TypeSchema()


