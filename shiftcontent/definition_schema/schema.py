from shiftschema import validators
from shiftschema import filters
from shiftcontent.definition_schema import validators as content_validators
from shiftcontent.definition_schema.base import BaseSchema


class DefinitionSchema(BaseSchema):
    """
    Content definition schema
    Used to validate content type definitions
    """
    def validate_collections(self, model, context=None):
        """
        Use definition as context for nested collections (types need that)
        """
        return super().validate_collections(model, model)

    def schema(self):
        self.add_collection('content')
        self.content.schema = TypeSchema()
        self.content.add_validator(validators.Required(
            message='Content types can\'t be empty'
        ))


class TypeSchema(BaseSchema):
    """
    Type schema
    Used to validate content types. This will be applied to every content type
    in the collection.
    """
    def validate_collections(self, model, context=None):
        """ Use type as context for nested collections (fields rely on that)"""
        return super().validate_collections(model, model)

    def schema(self):
        # content type name
        self.add_property('name')
        self.name.add_filter(filters.Strip())
        self.name.add_validator(validators.Required(
            message='Content type must have a name'
        ))
        self.name.add_validator(content_validators.UniqueTypeName())

        # content type handle
        self.add_property('handle')
        self.handle.add_filter(filters.Strip())
        self.handle.add_validator(validators.Required(
            message='Content type must have a handle'
        ))
        self.handle.add_validator(content_validators.Handle())
        self.handle.add_validator(content_validators.UniqueTypeHandle())

        # content type description
        self.add_property('description')
        self.description.add_filter(filters.Strip())
        self.description.add_validator(validators.Required(
            message='Content type needs a description'
        ))

        # content type editor
        self.add_property('editor')
        self.editor.add_filter(filters.Strip())
        self.editor.add_validator(content_validators.Importable(
            message='Content type editor [{name}] is not importable'
        ))

        # content type fields
        self.add_collection('fields')
        self.fields.schema = FieldSchema()
        self.fields.add_validator(validators.Required(
            message='Content type must have fields'
        ))


class FieldSchema(BaseSchema):
    """
    Field schema
    Used to validate fields attached to content types. This will be run for
    every field on every content type
    """
    def schema(self):
        # field name
        self.add_property('name')
        self.name.add_filter(filters.Strip())
        self.name.add_validator(content_validators.UniqueFieldName())
        self.name.add_validator(validators.Required(
            message='Field requires a name'
        ))

        # field handle
        self.add_property('handle')
        self.handle.add_filter(filters.Strip())
        self.handle.add_validator(content_validators.Handle())
        self.handle.add_validator(content_validators.UniqueFieldHandle())
        self.handle.add_validator(content_validators.NonMetafieldHandle())
        self.handle.add_validator(validators.Required(
            message='Field requires a handle'
        ))

        # field description
        self.add_property('description')
        self.description.add_filter(filters.Strip())

        # field type
        self.add_property('type')
        self.type.add_filter(filters.Strip())
        self.type.add_validator(validators.Required(
            message='Field requires a type'
        ))

        # field filters
        self.add_collection('filters')
        self.filters.schema = FilterSchema()

        # field validators
        self.add_collection('validators')
        self.validators.schema = ValidatorSchema()


class FilterSchema(BaseSchema):
    """
    Filter schema
    Used to validate filter definitions attached to content type fields.
    This will get run for every filter attached to every field.
    """
    def schema(self):
        self.add_property('type')
        self.type.add_validator(validators.Required(
            message='Filter requires a type'
        ))
        self.type.add_validator(content_validators.Importable(
            message='Filter class [{class}] is not importable'
        ))
        self.type.add_validator(content_validators.Instantiatable(
            message='Filter [{cls}] is not instantiatable with provided '
                    'parameters [{params}]'
        ))


class ValidatorSchema(BaseSchema):
    """
    Validator schema
    Used to validate validator definitions attached to content type fields.
    This will get run for every validator attached to every field.
    """
    def schema(self):
        self.add_property('type')
        self.type.add_validator(validators.Required(
            message='Validator requires a type'
        ))
        self.type.add_validator(content_validators.Importable(
            message='Validator class [{cls}] is not importable'
        ))
        self.type.add_validator(content_validators.Instantiatable(
            message='Validator [{cls}] is not instantiatable with provided '
                    'parameters [{params}]'
        ))



