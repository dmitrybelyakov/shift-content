from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemDelete(BaseHandler):
    """
    Delete content item
    This handler deletes existing content items.
    Expects the following payload structure:

    event = {
        ...
        payload=None,
        payload_rollback={
            type='plain_text',
            author=123,
            object_id='d2bf6e2c-aba6-11e8-89e5-38c9863edaea',
            custom_field='some value'
        }
    }

    """

    EVENT_TYPES = (
        'CONTENT_ITEM_DELETE',
    )

    def handle(self, event):
        """
        Handle event
        Delete content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.delete().where(
                items.c.object_id == event.object_id
            ))

        return event

    def rollback(self, event):
        """
        Rollback event
        Re-creates content item in the database
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        rollback_data = event.payload_rollback
        if 'id' in rollback_data:
            del rollback_data['id']

        item = Item(**rollback_data)

        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        return event





