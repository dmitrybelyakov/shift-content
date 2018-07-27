from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemIndex(BaseHandler):
    """
    Index content item
    Puts content item to index
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_CREATE',
        'CONTENT_ITEM_UPDATE',
        'CONTENT_ITEM_UPDATE_FIELD',
    )

    def handle(self, event):
        """
        Create content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        return event

    def rollback(self, event):
        """ Rollback event """
        return event





