class ContentException(Exception):
    """ Generic content exception marker """
    pass


class ConfigurationException(ContentException, RuntimeError):
    """ Raised when configuration is invald """
    pass

