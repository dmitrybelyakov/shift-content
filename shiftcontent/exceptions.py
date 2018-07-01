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


class UndefinedContentType(ContentException, RuntimeError):
    """ Raised when requesting schema for nonexistent content type """
    pass


class DatabaseError(ContentException, Exception):
    """ Generic database errors """
    pass


class EventError(DatabaseError, RuntimeError):
    """ Raised when there is an issue with event object """
    pass


class ProcessingUnsavedEvent(ContentException, RuntimeError):
    """ Raised when emitting or rolling back  unsaved event"""
    pass


class MissingEventType(ContentException, RuntimeError):
    """ Raised when handler implementation doesn't define EVENT_TYPE """
    pass


class UnsupportedEventType(ContentException, RuntimeError):
    """ Raised when running a handler with unsupported event type """
    pass


class HandlerInstantiationError(ContentException, RuntimeError):
    """ Raised when handlers are defined not as classes """
    pass


class ContentItemError(DatabaseError, RuntimeError):
    """ Raised when there is an issue with content item object """
    pass


class InvalidEvent(ContentException, RuntimeError):
    """ Raised when trying to persist invalid event """
    def __init__(self, *args, validation_errors=None, **kwargs):
        self.validation_errors = validation_errors
        super().__init__(*args, **kwargs)



