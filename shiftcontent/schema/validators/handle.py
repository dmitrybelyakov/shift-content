from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import re


class Handle(AbstractValidator):
    """
    Handle validator
    Checks that field and type handles are lowercase and do not contain illegal
    characters
    """

    invalid_name = 'Handle [{}] must start with a letter, and contain ' \
                   'numbers, lowercase letters and underscores only'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.invalid_name = message

    def validate(self, value, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        pattern = '^[a-z][a-z\d_]*'
        match = re.match(pattern, value)
        if not match or value != match.group():
            params = dict(handle=value)
            return Error(self.invalid_name, params)

        # success otherwise
        return Error()