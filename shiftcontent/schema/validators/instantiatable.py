from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from shiftcontent.utils import import_by_name


class Instantiatable(AbstractValidator):
    """
    Instantiatable
    Checks that filters and validators are instantiatable with all the
    parameters provided in the schema
    """

    not_instantiatable = 'Class [{cls}] is not instantiatable with ' \
                         'provided parameters [{params}]'

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
        params = {p: v for p, v in model.items() if p != 'type'}
        error_params = dict(cls=value, params=', '.join(params.keys()))

        try:
            imported = import_by_name(value)
            imported(**params)
        except TypeError:
            return Error(self.not_instantiatable, error_params)
        except ImportError:
            return Error(self.not_instantiatable, error_params)

        # success otherwise
        return Error()