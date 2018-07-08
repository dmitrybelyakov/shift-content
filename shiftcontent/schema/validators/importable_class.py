from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from functools import reduce


class ImportableClass(AbstractValidator):
    """
    Importable class
    Checks that a class defined in schema can be imported
    """

    not_importable = 'Class [{}] is not importable.'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.handle_not_unique = message

    def validate(self, value, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """


        # success otherwise
        return Error()