from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from functools import reduce


class UniqueTypeHandle(AbstractValidator):
    """
    Unique type handle
    Checks that content type handle is unique and not repeated
    """

    handle_not_unique = 'Content type handle [{handle}] is not unique'

    def __init__(self, message=None):
        """
        Instantiates validator and can optionally accept a custom error
        message value
        :param message: str, custom error message
        """
        if message:
            self.handle_not_unique = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param model: obj or None, model being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        count = 0
        types = context['content'] if context and 'content' in context else None
        if types:
            val = value
            count = reduce(
                lambda a, c: a+1 if 'handle' in c and c['handle'] == val else a,
                types,
                0
            )

        # more than 1 occurrence
        if count > 1:
            params = dict(handle=value)
            return Error(self.handle_not_unique, params)

        # success otherwise
        return Error()