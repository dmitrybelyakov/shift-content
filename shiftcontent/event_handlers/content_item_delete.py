from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemDelete(BaseHandler):
    """
    Delete content item
    This handler deletes existing content items
    """

    EVENT_TYPE = 'CONTENT_ITEM_DELETE'

    def handle(self, event):
        """
        Create content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        print('DELETE CONTENT ITEM')

        # type = event.payload['type']
        # del event.payload['type']
        # item = Item(
        #     type=type,
        #     **event.payload
        # )
        #
        # items = db.tables['items']
        # with db.engine.begin() as conn:
        #     result = conn.execute(items.insert(), **item.to_db())
        #     item.id = result.inserted_primary_key[0]
        #
        # return event

    def rollback(self, event):
        """ Rollback event """
        print('ROLLBACK ITEM DELETE')
        # items = db.tables['items']
        # with db.engine.begin() as conn:
        #     query = items.delete()\
        #         .where(items.c.object_id == event.object_id)
        #     conn.execute(query)
        #
        # return event





