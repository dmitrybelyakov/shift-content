from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
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
        Create content item and return an event for further
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
        """ Rollback event """
        print('ADD ITEM BACK TO INDEX')
        return event





