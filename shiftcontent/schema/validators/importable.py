from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import sys
from importlib import import_module


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

    def import_by_name(self, name):
        """
        Import by name
        Accepts to import module, object, class, function or variable.
        :param name: str, what to import
        :return: import target
        """
        # try as module
        try:
            return import_module(name)
        except ImportError:
            if '.' not in name:
                raise

        # recursively find a module
        module_name, obj = name.rsplit('.', 1)
        try:
            module = import_module(module_name)
        except ImportError:
            module = self.import_by_name(module_name)

        # now get object as module's attribute
        try:
            return getattr(module, obj)
        except AttributeError as e:
            raise ImportError(e)

    def validate(self, value, context=None):
        """
        Validate
        Performs validation and return an error object

        :param value: str, value being validated
        :param context: obj or None, validation context
        :return: shiftschema.results.SimpleResult
        """

        try:
            self.import_by_name(value)
        except ImportError:
            params = dict(name=value)
            return Error(self.not_importable, params)

        # success otherwise
        return Error()

