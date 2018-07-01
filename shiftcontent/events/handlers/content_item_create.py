from shiftcontent.events.handlers import BaseHandler
from shiftcontent.item import Item


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

        # create item
        item = Item(
            author=event.author,
            object_id=event.object_id,
            type=event.payload['type'],
            data=event.payload['data']
        )

        # persist
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        return event

    def rollback(self, event):
        """ Rollback event """
        payload = event.payload
        if 'dummy_handler1' in payload:
            del payload['dummy_handler1']

        event.payload = payload
        return event


