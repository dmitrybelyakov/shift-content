from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemUpdate(BaseHandler):
    """
    Update content item
    This handler saves updates to existing content items
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_UPDATE',
    )

    def handle(self, event):
        """
        Handle event
        Update content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        type = event.payload['meta']['type']
        del event.payload['meta']['type']
        item = Item(type=type, **event.payload)
        db_data = item.to_db()

        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.update().where(items.c.object_id == event.object_id)
            conn.execute(query.values(**db_data))

        return event

    def rollback(self, event):
        """
        Rollback event
        Rollback changes using before-update dta save in payload.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        type = event.payload_rollback['meta']['type']
        del event.payload_rollback['meta']['type']
        item = Item(type=type, **event.payload_rollback)
        db_data = item.to_db()

        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.update().where(items.c.object_id == event.object_id)
            conn.execute(query.values(**db_data))





