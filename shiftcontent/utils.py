from importlib import import_module
from mprop import mproperty


def import_by_name(name):
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
        module = import_by_name(module_name)

    # now get object as module's attribute
    try:
        return getattr(module, obj)
    except AttributeError as e:
        raise ImportError(e)


def mprop(func):
    """
    Method-levelmproperty decorator
    Wraps around mproperty decorator to hold the reference to instance.
    This ensures it doesn't get instantiated more than once and on subsequent
    access we return already instantiated object.
    :param func: function to wrap
    :return:
    """
    instance = None

    def stateful_wrapper():
        return instance if instance else mproperty(func)
    return stateful_wrapper()