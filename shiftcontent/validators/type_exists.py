from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import re


class TypeExists(AbstractValidator):
    """
    Type exists validator
    Checks that content type assigned to an item exists in schema
    """

    type_doesnt_exist = 'Content type [{type}] does not exist.'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.invalid_name = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param model: obj or None, model being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        schema = context['content_schema']
        if value not in schema.keys():
            params = dict(type=value)
            return Error(self.type_doesnt_exist, params)

        # success otherwise
        return Error()