from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import search_service
from shiftcontent import cache_service
from pprint import pprint as pp


class ContentItemCreate(BaseHandler):
    """
    Create content item
    This handler creates a new content item entry.
    Expects the following payload structure:

    event = {
        ...
        payload={
            type='plain_text',
            author=123,
            object_id='d2bf6e2c-aba6-11e8-89e5-38c9863edaea',
            custom_field='some value'
        },
        payload_rollback=None
    }
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_CREATE',
    )

    def handle(self, event):
        """
        Handle event
        Create content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        # create
        item = Item(**event.payload)
        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            event.object_id = item.object_id
            item.set_field(
                'id',
                initial=True,
                value=result.inserted_primary_key[0]
            )

        # cache
        cache_service.set(item)

        # index
        search_service.put_to_index(item)

        return event

    def rollback(self, event):
        """
        Rollback event
        Removes created content item
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        from shiftcontent import content_service
        item = content_service.get_item(event.object_id)
        if not item:
            return event

        # delete
        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.delete()\
                .where(items.c.object_id == event.object_id)
            conn.execute(query)

        # remove from cache
        cache_service.delete(item.object_id)

        # remove from index
        search_service.delete(item.type, item.object_id)

        return event





