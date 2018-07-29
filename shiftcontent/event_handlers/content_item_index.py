from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import search_service
from elasticsearch import exceptions as ex
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
        # get item
        object_id = event.object_id
        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            data = conn.execute(query).fetchone()
            if data:
                item = Item(**data)
            else:
                return event

        # index
        try:
            search_service.put_to_index(item)
        except ex.ImproperlyConfigured:
            pass

        # and return
        return event

    def rollback(self, event):
        """ Rollback event """
        print('RE-INDEX CONTENT ITEM')
        return event





