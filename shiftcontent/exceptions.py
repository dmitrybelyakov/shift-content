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
    """ Raised when adding a bad schema revision file to regsitry """
    pass


class InvalidItemSchemaType(ContentException, RuntimeError):
    """ Raised when requested creation of item schema with bad type """
    pass


class UndefinedContentType(ContentException, RuntimeError):
    """ Raised when discovered a nonexistent content type  """
    pass


class DatabaseError(ContentException, Exception):
    """ Generic database errors """
    pass


class ContentItemError(DatabaseError, RuntimeError):
    """ Raised when there is an issue with content item object """
    pass


class InvalidEvent(ContentException, RuntimeError):
    """ Raised when trying to persist invalid event """
    def __init__(self, *args, validation_errors=None, **kwargs):
        self.validation_errors = validation_errors
        super().__init__(*args, **kwargs)



