from shiftschema.schema import Schema


class BaseSchema(Schema):
    """
    Base content schema
    This will override validation and filtering rules to always pass current
    model as context to nested collections and entities.
    """
    def filter_entities(self, model, context=None):
        super().filter_entities(model, model)

    def filter_context(self, model, context=None):
        super().filter_entities(model, model)

    def validate_entities(self, model, context=None):
        return super().validate_entities(model, model)

    def validate_collections(self, model, context=None):
        return super().validate_collections(model, model)