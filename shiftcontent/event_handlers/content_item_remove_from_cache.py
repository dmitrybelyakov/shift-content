from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftmemory import exceptions as cx
from pprint import pprint as pp


class ContentItemRemoveFromCache(BaseHandler):
    """
    Remove content item from index
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_DELETE',
    )

    def handle(self, event):
        """
        Handle event
        Removes content item From cache and return an event for further
        handler chaining.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        try:
            cache_service.delete(event.object_id)
        except cx.ConfigurationException:
            pass

        return event

    def rollback(self, event):
        """
        Rollback event
        Re-add content item to cache

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        item = Item(
            type=event.payload_rollback['meta']['type'],
            **event.payload_rollback
        )

        try:
            cache_service.set(item)
        except cx.ConfigurationException:
            pass

        return event





