from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from shiftcontent.utils import import_by_name


class IsList(AbstractValidator):
    """
    Is list
    Checks that validated value is a list
    """

    not_a_list = 'Invalid value, must be a list, got [{type}]'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.not_a_list = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param model: obj or None, validation context
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        if type(value) is not list:
            params = dict(type=type(value))
            return Error(self.not_a_list, params)

        # success otherwise
        return Error()

