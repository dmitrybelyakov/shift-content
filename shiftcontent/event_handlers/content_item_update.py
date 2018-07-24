from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from pprint import pprint as pp


class ContentItemUpdate(BaseHandler):
    """
    Update content item
    This handler saves updates to existing content items
    """

    EVENT_TYPE = 'CONTENT_ITEM_UPDATE'

    def handle(self, event):
        """
        Update content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        type = event.payload['meta']['type']
        del event.payload['meta']['type']
        item = Item(type=type, **event.payload)
        item.created_string = item.created
        db_data = item.to_db()
        del db_data['object_id']
        del db_data['id']

        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.update().where(items.c.object_id == event.object_id)
            conn.execute(query.values(**db_data))

        return event

    def rollback(self, event):
        """ Rollback event """
        print('ROLLBACK CONTENT ITEM UPDATE')
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





