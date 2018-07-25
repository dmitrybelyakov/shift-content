from importlib import import_module


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



