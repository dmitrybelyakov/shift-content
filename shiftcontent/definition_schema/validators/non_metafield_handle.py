from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from functools import reduce
from shiftcontent.item import Item


class NonMetafieldHandle(AbstractValidator):
    """
    Non Metafield Handle
    Checks that field handle we intend to use is not reserved for
    metafields.
    """

    metafield = 'Content field handle [{handle}] is reserve for metadata'

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
        if value in Item.valid_metafields:
            params = dict(handle=value)
            return Error(self.metafield, params)

        # success otherwise
        return Error()