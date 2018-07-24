from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemFieldUpdateField(BaseHandler):
    """
    Update content item field
    This handler updates single field on a content item
    """

    EVENT_TYPE = 'CONTENT_ITEM_UPDATE_FIELD'

    def handle(self, event):
        """
        Update content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        print('UPDATE CONTENT ITEM FIELD')
        pp(event)
        # items = db.tables['items']
        # with db.engine.begin() as conn:
        #     conn.execute(items.delete().where(
        #         items.c.object_id == event.object_id
        #     ))
        #
        # return event

    def rollback(self, event):
        """ Rollback event """
        print('ROLLBACK CONTENT ITEM FIELD UPDATE')
        pp(event)
        # rollback_data = event.payload_rollback
        # if 'id' in rollback_data:
        #     del rollback_data['id']
        #
        # type = rollback_data['meta']['type']
        # del rollback_data['meta']['type']
        #
        # item = Item(type=type, **rollback_data)
        # item.created_string = event.payload_rollback['meta']['created']
        #
        # items = db.tables['items']
        # with db.engine.begin() as conn:
        #     result = conn.execute(items.insert(), **item.to_db())
        #     item.id = result.inserted_primary_key[0]
        #
        # return event





