from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import search_service
from elasticsearch import exceptions as ex
from pprint import pprint as pp


class ContentItemIndex(BaseHandler):
    """
    Index content item
    Puts content item to index.
    Expects the following payload structure:
    event = {
        ...
        payload=None (ignored),
        payload_rollback=None (ignored)
    }
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_CREATE',
        'CONTENT_ITEM_UPDATE',
        'CONTENT_ITEM_UPDATE_FIELD',
    )

    def index(self, object_id):
        """
        Index
        Retrieves item from the database and puts it to search index.
        This will be used in both handle and rollback as they essentially
        do the same thing.

        :param object_id: str, item id (must be in the database)
        :return: None
        """
        from shiftcontent import content_service
        item = content_service.get_item(object_id)
        if item:
            search_service.put_to_index(item)

    def handle(self, event):
        """
        Handle event
        Add content item to index and return an event for further handler
        chaining. We do need to get item from database here because some events,
        e.g. field update, don't carry enough payload to create full item index.
        This makes this handler more universal.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        self.index(event.object_id)
        return event

    def rollback(self, event):
        """
        Rollback event
        Simply re-indexes content item. This will get run later in the handlers
        chain, thus we can assume item was properly rolled back at this point.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        self.index(event.object_id)
        return event





