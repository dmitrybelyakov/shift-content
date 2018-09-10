from shiftevent.handlers.base import BaseHandler
from shiftcontent import db
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

    def handle(self, event):
        """
        Handle event
        Update content item and return an event for further
        handler chaining.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        items = db.tables['items']

        field = event.payload['field']
        value = event.payload['value']
        metafield = event.payload['metafield']

        # update metafield
        if metafield:
            values = dict()
            values[field] = value
            query = items.update().where(items.c.object_id == event.object_id)
            with db.engine.begin() as conn:
                conn.execute(query.values(**values))

        # update custom field
        if not metafield:
            select = items.select().where(items.c.object_id == event.object_id)
            update = items.update().where(items.c.object_id == event.object_id)
            with db.engine.begin() as conn:
                item = conn.execute(select).fetchone()
                fields = json.loads(item.fields, encoding='utf-8')
                fields[field] = value
                fields = json.dumps(fields, ensure_ascii=False)
                conn.execute(update.values(fields=fields))

        return event

    def rollback(self, event):
        """
        Rollback event
        Reverts changes to field using before-update data stored in payload.
        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        items = db.tables['items']

        field = event.payload_rollback['field']
        value = event.payload_rollback['value']
        metafield = event.payload['metafield']

        # rollback metafield
        if metafield:
            values = dict()
            values[field] = value
            query = items.update().where(items.c.object_id == event.object_id)
            with db.engine.begin() as conn:
                conn.execute(query.values(**values))

        # rollback custom field
        if not metafield:
            select = items.select().where(items.c.object_id == event.object_id)
            update = items.update().where(items.c.object_id == event.object_id)
            with db.engine.begin() as conn:
                item = conn.execute(select).fetchone()
                fields = json.loads(item.fields, encoding='utf-8')
                fields[field] = value
                fields = json.dumps(fields, ensure_ascii=False)
                conn.execute(update.values(fields=fields))

        return event





