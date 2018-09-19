from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import search_service
from shiftcontent import cache_service
from pprint import pprint as pp
import json


class ContentItemFieldUpdateField(BaseHandler):
    """
    Update content item field
    This handler updates single field on a content item.

    Expects the following payload structure:
    event = {
        ...
        payload={
            metafield=True,
            field='path',
            value='new value'
        },
        payload_rollback={
            metafield=True,
            field='path',
            value='old value'
        },
    }

    """

    EVENT_TYPES = (
        'CONTENT_ITEM_UPDATE_FIELD',
    )


    def update_field(self, object_id, field, value, metafield):
        """
        Update field
        Performs database update setting a new value on a field.
        This was extracted to be used from both handle and rollback methods.
        Will return updated item data on success.

        :param object_id: str, object_id of the item
        :param field: str, field name to update
        :param value: mixed, new value to set
        :param metafield: bool, whether the field is a metafield
        :return: dict
        """
        items = db.tables['items']
        with db.engine.begin() as conn:

            select = items.select().where(items.c.object_id == object_id)
            update = items.update().where(items.c.object_id == object_id)

            # update metafield
            if metafield:
                values = dict()
                values[field] = value
                conn.execute(update.values(**values))

            # update custom field
            if not metafield:
                item_data = conn.execute(select).fetchone()
                fields = json.loads(item_data.fields, encoding='utf-8')
                fields[field] = value
                fields = json.dumps(fields, ensure_ascii=False)
                conn.execute(update.values(fields=fields))

            # get updated item data
            item_data = conn.execute(select).fetchone()

        # and return
        return item_data

    def handle(self, event):
        """
        Handle event
        Update content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        item_data = self.update_field(
            object_id=event.object_id,
            field=event.payload['field'],
            value=event.payload['value'],
            metafield=event.payload['metafield']
        )

        # prepare item
        item = Item().from_db(item_data)

        # cache
        cache_service.set(item)

        # index
        search_service.put_to_index(item)

        return event

    def rollback(self, event):
        """
        Rollback event
        Reverts changes to field using before-update data stored in payload.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        item_data = self.update_field(
            object_id=event.object_id,
            field=event.payload_rollback['field'],
            value=event.payload_rollback['value'],
            metafield=event.payload_rollback['metafield']
        )

        # prepare item
        item = Item().from_db(item_data)

        # cache
        cache_service.set(item)

        # index
        search_service.put_to_index(item)

        return event





