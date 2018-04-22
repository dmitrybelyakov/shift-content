class ContentException(Exception):
    """ Generic content exception marker """
    pass


class ConfigurationException(ContentException, RuntimeError):
    """ Raised when configuration is invalid """
    pass


class InvalidSchema(ContentException, RuntimeError):
    """ Raised when loaded schema definition is invalid """
    def __init__(self, *args, validation_errors=None, **kwargs):
        self.validation_errors = validation_errors
        super().__init__(*args, **kwargs)


class UnableToRegisterSchemaRevision(ContentException, RuntimeError):
    """ Raised when ading a bad schema revision file to regsitry """
    pass

