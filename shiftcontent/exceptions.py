class ContentException(Exception):
    """ Generic content exception marker """
    pass


class ConfigurationException(ContentException, RuntimeError):
    """ Raised when configuration is invalid """
    pass


class InvalidDefinition(ContentException, RuntimeError):
    """ Raised when loaded definition is invalid """
    def __init__(self, *args, validation_errors=None, **kwargs):
        self.validation_errors = validation_errors
        super().__init__(*args, **kwargs)


class UnableToRegisterRevision(ContentException, RuntimeError):
    """ Raised when adding a bad definition revision file to registry """
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


class ItemError(ContentException, RuntimeError):
    """ Raised when there is an issue with content item object """
    pass


class ItemNotFound(ContentException, RuntimeError):
    """ Raised when performing operations on nonexistent items """
    pass







