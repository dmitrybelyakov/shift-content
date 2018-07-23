from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent.services import db


class ContentItemCreate(BaseHandler):
    """
    Create content item
    This handler creates a new content item entry.
    """

    EVENT_TYPE = 'CONTENT_ITEM_CREATE'

    def handle(self, event):
        """
        Create content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        item = Item(
            fields=(),
            **event.payload
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        return event

    def rollback(self, event):
        """ Rollback event """
        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.delete()\
                .where(items.c.object_id == event.object_id)
            conn.execute(query)

        return event





