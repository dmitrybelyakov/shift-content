from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from pprint import pprint as pp


class FieldType(AbstractValidator):
    """
    Field type
    Checks that field type defined for a field actually exists
    """

    invalid_type = 'Field type [{field_type}] does not exist'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.invalid_type = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param model: obj or None, model being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        from shiftcontent import definition_service
        types = definition_service.field_types()

        # error if not found
        if value not in types.keys():
            params = dict(field_type=value)
            return Error(self.invalid_type, params)

        # success otherwise
        return Error()

