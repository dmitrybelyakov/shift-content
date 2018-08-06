from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import cache_service
from shiftmemory import exceptions as cx
from pprint import pprint as pp


class ContentItemCache(BaseHandler):
    """
    Cache content item
    Puts content item into cache
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_CREATE',
        'CONTENT_ITEM_UPDATE',
        'CONTENT_ITEM_UPDATE_FIELD',
    )

    def handle(self, event):
        """
        Handle event
        Add content item to cache and return an event for further handler
        chaining. We do need to get item from database here because some events,
        e.g. field update, don't carry enough payload to create full item.
        This makes this handler more universal.

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
                item = Item()
                item.from_db(data)
            else:
                return event  # skip if not found (e.g. rolling back creation)

        # cache
        try:
            cache_service.set(item)
        except cx.ConfigurationException:
            pass

        # and return
        return event

    def rollback(self, event):
        """
        Rollback event
        Simply recreates item cache. This will get run later in the handlers
        chain, thus we can assume item was properly rolled back at this point.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        return self.handle(event)





