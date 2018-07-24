from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from shiftcontent.utils import import_by_name


class Importable(AbstractValidator):
    """
    Importable class
    Checks that a class defined in schema can be imported
    """

    not_importable = 'Import failed: [{name}] is not importable.'

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
        :param model: obj or None, validation context
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """
        try:
            import_by_name(value)
        except ImportError:
            params = dict(name=value)
            return Error(self.not_importable, params)

        # success otherwise
        return Error()

