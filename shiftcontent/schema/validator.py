from shiftschema.schema import Schema
from shiftschema import validators as validator
from shiftschema import filters as filter

from shiftcontent.schema import validators as content_validators


class DefinitionSchema(Schema):
    """
    Content definition schema
    Used to validate content type definitions
    """
    def schema(self):
        self.add_collection('content')
        self.content.schema = TypeSchema()


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

        # content type fields
        self.add_collection('fields')
        self.fields.schema = FieldSchema()
        self.fields.add_validator(validator.NotEmpty(
            message='Content type must have fields'
        ))





class FieldSchema(Schema):
    """
    Field schema
    Used to validate fields attached to content types. This will be run for
    every field on every content type
    """
    def schema(self):
        # field name
        self.add_property('name')
        self.name.add_filter(filter.Strip())
        self.name.add_validator(validator.Required())
        self.name.add_validator(content_validators.UniqueTypeName())

        # field handle
        self.add_property('handle')
        self.handle.add_filter(filter.Strip())
        self.handle.add_filter(filter.Lowercase())
        self.handle.add_validator(validator.Required())
        self.handle.add_validator(content_validators.UniqueTypeHandle())

        # field description
        self.add_property('description')
        self.description.add_filter(filter.Strip())
        self.description.add_validator(validator.Required())

        # field type
        self.add_property('type')
        self.type.add_filter(filter.Strip())
        self.type.add_validator(validator.Required())


class FilterSchema(Schema):
    """
    Filter schema
    Used to validate filter definitions attached to content type fields.
    This will get run for every filter attached to every field.
    """
    pass


class ValidatorSchema(Schema):
    """
    Validator schema
    Used to validate validator definitions attached to content type fields.
    This will get run for every validator attached to every field.
    """
    pass



