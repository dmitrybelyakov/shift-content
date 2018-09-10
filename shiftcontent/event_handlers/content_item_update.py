from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemUpdate(BaseHandler):
    """
    Update content item
    This handler saves updates to existing content items.

    Expects the following payload structure:
    event = {
        ...
        payload={
            type='plain_text',
            author=123,
            object_id='d2bf6e2c-aba6-11e8-89e5-38c9863edaea',
            custom_field='new value'
        },
        payload_rollback={
            type='plain_text',
            author=123,
            object_id='d2bf6e2c-aba6-11e8-89e5-38c9863edaea',
            custom_field='old value'
        },
    }

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
        item = Item()
        item.from_json(event.payload_json)
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
        item = Item()
        item.from_json(event.payload_rollback_json)
        db_data = item.to_db()
        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.update().where(items.c.object_id == event.object_id)
            conn.execute(query.values(**db_data))





