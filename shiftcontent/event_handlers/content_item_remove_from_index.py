from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import search_service
from elasticsearch import exceptions as ex
from pprint import pprint as pp


class ContentItemRemoveFromIndex(BaseHandler):
    """
    Remove content item from index
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_DELETE',
    )

    def handle(self, event):
        """
        Handle event
        Removes content item From index and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        try:
            search_service.delete(event.object_id)
        except ex.ImproperlyConfigured:
            pass

        return event

    def rollback(self, event):
        """
        Rollback event
        Re-add content item to index
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        item = Item(
            type=event.payload_rollback['meta']['type'],
            **event.payload_rollback
        )

        # index
        try:
            search_service.put_to_index(item)
        except ex.ImproperlyConfigured:
            pass





