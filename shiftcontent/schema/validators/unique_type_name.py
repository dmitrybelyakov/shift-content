from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from functools import reduce

class UniqueTypeName(AbstractValidator):
    """
    Unique type name
    Checks that content type name is unique and not repeated
    """

    name_not_unique = 'Content type name [{name}] is not unique'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.name_not_unique = message

    def validate(self, value, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        count = 0
        types = context['content'] if 'content' in context else None
        if types:
            count = reduce(
                lambda a, c: a + 1 if c['name'] == value else a,
                types,
                0
            )

        # more than 1 occurrence
        if count > 1:
            params = dict(name=value)
            return Error(self.name_not_unique, params)

        # success otherwise
        return Error()