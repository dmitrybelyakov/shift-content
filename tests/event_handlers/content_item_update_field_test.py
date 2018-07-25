from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemFieldUpdateField
from shiftcontent.item import Item
from shiftcontent import db


@attr('event', 'handler', 'content_item_update_field')
class ContentItemUpdateFieldTest(BaseTestCase):

    def test_instantiating_handler(self):
        """ Instantiating content item create handler """
        handler = ContentItemFieldUpdateField(db=self.db)
        self.assertIsInstance(handler, ContentItemFieldUpdateField)

    def test_handle_field(self):
        """ Content item update field: handle field"""
        items = db.tables['items']

        author = '123'
        object_id = str(uuid1())

        item = Item('plain_text', **dict(
            author=author,
            object_id=object_id,
            body='Initial body'
        ))
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=author,
            object_id=object_id,
            payload=dict(
                metafield=False,
                field='body',
                value='Updated body'
            ),
            payload_rollback=dict(
                metafield=False,
                field='body',
                value='Initial body'
            )
        )

        handler = ContentItemFieldUpdateField(db=self.db)
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item(**record)
            self.assertEquals('Updated body', updated.body)

    def test_rollback_field(self):
        """ Content item update field: rollback  field"""
        items = db.tables['items']

        author = '123'
        object_id = str(uuid1())

        item = Item('plain_text', **dict(
            author=author,
            object_id=object_id,
            body='Initial body'
        ))
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=author,
            object_id=object_id,
            payload=dict(
                metafield=False,
                field='body',
                value='Updated body'
            ),
            payload_rollback=dict(
                metafield=False,
                field='body',
                value='Initial body'
            )
        )

        handler = ContentItemFieldUpdateField(db=self.db)
        handler.handle(event)
        handler.rollback(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item(**record)
            self.assertEquals('Initial body', updated.body)

    def test_handle_metafield(self):
        """ Content item update field: handle metafield"""
        items = db.tables['items']

        author = '123'
        new_author = '456'
        object_id = str(uuid1())

        item = Item('plain_text', **dict(
            author=author,
            object_id=object_id,
            body='Initial body'
        ))
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=author,
            object_id=object_id,
            payload=dict(
                metafield=True,
                field='author',
                value=new_author
            ),
            payload_rollback=dict(
                metafield=True,
                field='author',
                value=author
            )
        )

        handler = ContentItemFieldUpdateField(db=self.db)
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item(**record)
            self.assertEquals(new_author, updated.author)

    def test_rollback_metafield(self):
        """ Content item update field: rollback  metafield"""
        items = db.tables['items']

        author = '123'
        new_author = '456'
        object_id = str(uuid1())

        item = Item('plain_text', **dict(
            author=author,
            object_id=object_id,
            body='Initial body'
        ))
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=author,
            object_id=object_id,
            payload=dict(
                metafield=True,
                field='author',
                value=new_author
            ),
            payload_rollback=dict(
                metafield=True,
                field='author',
                value=author
            )
        )

        handler = ContentItemFieldUpdateField(db=self.db)
        handler.handle(event)
        handler.rollback(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item(**record)
            self.assertEquals(author, updated.author)


