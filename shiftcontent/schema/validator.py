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
        self.content.add_validator(validator.Required(
            message='Content types can\'t be empty'
        ))


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
        self.name.add_validator(validator.Required(
            message='Content type must have a name'
        ))
        self.name.add_validator(content_validators.UniqueTypeName())

        # content type handle
        self.add_property('handle')
        self.handle.add_filter(filter.Strip())
        self.handle.add_validator(validator.Required(
            message='Content type must have a handle'
        ))
        self.handle.add_validator(content_validators.Handle())
        self.handle.add_validator(content_validators.UniqueTypeHandle())

        # content type description
        self.add_property('description')
        self.description.add_filter(filter.Strip())
        self.description.add_validator(validator.Required(
            message='Content type needs a description'
        ))

        # content type editor
        self.add_property('editor')
        self.editor.add_filter(filter.Strip())
        self.editor.add_validator(content_validators.ImportableClass())

        # content type fields
        self.add_collection('fields')
        self.fields.schema = FieldSchema()
        self.fields.add_validator(validator.Required(
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
        self.name.add_validator(validator.Required(
            message='Field requires a name'
        ))
        # todo: name must be unique

        # field handle
        self.add_property('handle')
        self.handle.add_filter(filter.Strip())
        self.handle.add_validator(content_validators.Handle())
        self.handle.add_validator(validator.Required(
            message='Field requires a handle'
        ))
        # todo: handle must be unique

        # field description
        self.add_property('description')
        self.description.add_filter(filter.Strip())

        # field type
        self.add_property('type')
        self.type.add_filter(filter.Strip())
        self.type.add_validator(validator.Required(
            message='Field requires a type'
        ))

        # field filters
        self.add_collection('filters')
        self.filters.schema = FilterSchema()

        # field validators
        self.add_collection('validators')
        self.validators.schema = ValidatorSchema()


class FilterSchema(Schema):
    """
    Filter schema
    Used to validate filter definitions attached to content type fields.
    This will get run for every filter attached to every field.
    """
    def schema(self):
        self.add_property('type')
        self.type.add_filter(filter.Strip())
        self.type.add_validator(validator.Required())
        self.type.add_validator(content_validators.ImportableClass(
            message='Filter class [{class}] is not importable'
        ))


class ValidatorSchema(Schema):
    """
    Validator schema
    Used to validate validator definitions attached to content type fields.
    This will get run for every validator attached to every field.
    """
    def schema(self):
        self.add_property('type')
        self.type.add_filter(filter.Strip())
        self.type.add_validator(validator.Required())
        self.type.add_validator(content_validators.ImportableClass(
            message='Validator class [{class}] is not importable'
        ))



