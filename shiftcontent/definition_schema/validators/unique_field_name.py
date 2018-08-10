from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from functools import reduce


class UniqueFieldName(AbstractValidator):
    """
    Unique field name
    Checks that content type field name is unique and not repeated
    """

    name_not_unique = 'Content field name [{name}] is not unique'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.name_not_unique = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param model: obj or None, model being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        fields = context['fields'] if context and 'fields' in context else ()
        count = reduce(
            lambda a, c: a + 1 if 'name' in c and c['name'] == value else a,
            fields,
            0
        )

        # more than 1 occurrence
        if count > 1:
            params = dict(name=value)
            return Error(self.name_not_unique, params)

        # success otherwise
        return Error()