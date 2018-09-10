from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftcontent import db
from pprint import pprint as pp


class ContentItemRemoveFromCache(BaseHandler):
    """
    Remove content item from index.
    Expects the following payload structure:
    event = {
        ...
        payload=None,
        payload_rollback=None
    }

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
        cache_service.delete(event.object_id)
        return event

    def rollback(self, event):
        """
        Rollback event
        Re-add content item to cache

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        object_id = event.object_id
        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            data = conn.execute(query).fetchone()
            print('GOT DATA?')
            if data:
                item = Item()
                item.from_db(data)
                cache_service.set(item)

        return event





