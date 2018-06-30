import abc


class BaseHandler(metaclass=abc.ABCMeta):
    """
    Base event handler
    This enforces all event handlers to have a common interface and ensures
    all handlers have access to preconfigured environment objects like
    the database, cache, elastic search etc
    """

    # database instance
    db = None

    # cache service instance
    cache = None

    def __init__(self, db):
        """
        Initializes the handler and gets all required service injected
        :param db: shiftcontent.db.db.Db
        """
        self.db = db

    @abc.abstractmethod
    def handle(self, event):
        """
        Process an event
        This should be implemented in concrete handler. It will get triggered
        once an event is emitted.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        raise NotImplemented('Implement me in your concrete handler')

    @abc.abstractmethod
    def rollback(self, event):
        """
        Rollback an event
        This should be implemented in concrete handler. It will get triggered
        once a travel back in time is requested and we have to sequentially
        undo events effectively reverting the changes made.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        raise NotImplemented('Implement me in your concrete handler')
