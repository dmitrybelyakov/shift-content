from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.event_handlers import ContentItemFieldUpdateField
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import cache_service
from shiftcontent import search_service


@attr('event', 'handler', 'content_item_update_field')
class ContentItemUpdateFieldTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        cache_service.init()
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_prefix='content_tests'
        )

    def tearDown(self):
        """ Clean up """
        search_service.drop_all_indices()
        search_service.disconnect()
        cache_service.drop_cache(cache_service.cache_name)
        super().tearDown()

    # -------------------------------------------------------------------------
    # Tests
    # -------------------------------------------------------------------------

    def test_instantiating_handler(self):
        """ Instantiating content item update field handler """
        handler = ContentItemFieldUpdateField()
        self.assertIsInstance(handler, ContentItemFieldUpdateField)

    def test_handle_field(self):
        """ Content item update field: handle field"""
        items = db.tables['items']

        author = '123'
        object_id = str(uuid1())

        item = Item(
            type='plain_text',
            author=author,
            object_id=object_id,
            body='Initial body'
        )
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
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

        handler = ContentItemFieldUpdateField()
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item()
            updated.from_db(record)
            self.assertEquals('Updated body', updated.body)

    def test_handle_metafield(self):
        """ Content item update field: handle metafield"""
        items = db.tables['items']

        author = '123'
        new_author = '456'
        object_id = str(uuid1())

        item = Item(
            type='plain_text',
            author=author,
            object_id=object_id,
            body='Initial body'
        )
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
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

        handler = ContentItemFieldUpdateField()
        handler.handle(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item()
            updated.from_db(record)
            self.assertEquals(new_author, updated.author)

    def test_update_field_updates_cache(self):
        """ Update field handler updates cache """
        object_id = str(uuid1())
        type = 'plain_text'

        # create item
        item = Item(
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )
        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in cache
        self.assertIsNone(cache_service.get(object_id))

        # now trigger event
        handler = ContentItemFieldUpdateField()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=123,
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
        ))

        # assert in cache now
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cached)
        self.assertEquals('Updated body', cached.body)

    def test_update_field_updates_index(self):
        """ Update field handler updates index """
        object_id = str(uuid1())
        type = 'plain_text'

        # create item
        item = Item(
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )
        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in index
        self.assertIsNone(search_service.get(type, object_id))

        # now trigger event
        handler = ContentItemFieldUpdateField()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=123,
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
        ))

        # assert in index now
        found = search_service.get(type, object_id)
        self.assertIsNotNone(found)
        self.assertEquals('Updated body', found['_source']['body'])

    def test_rollback_field(self):
        """ Content item update field: rollback  field"""
        items = db.tables['items']

        author = '123'
        object_id = str(uuid1())

        item = Item(
            type='plain_text',
            author=author,
            object_id=object_id,
            body='Initial body'
        )
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
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

        handler = ContentItemFieldUpdateField()
        handler.handle(event)
        handler.rollback(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item()
            updated.from_db(record)
            self.assertEquals('Initial body', updated.body)

    def test_rollback_metafield(self):
        """ Content item update field: rollback  metafield"""
        items = db.tables['items']

        author = '123'
        new_author = '456'
        object_id = str(uuid1())

        item = Item(
            type='plain_text',
            author=author,
            object_id=object_id,
            body='Initial body'
        )
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
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

        handler = ContentItemFieldUpdateField()
        handler.handle(event)
        handler.rollback(event)

        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            record = conn.execute(query).fetchone()
            updated = Item()
            updated.from_db(record)
            self.assertEquals(author, updated.author)

    def test_update_field_rollback_updates_cache(self):
        """ Update field rollback updates cache """
        object_id = str(uuid1())
        type = 'plain_text'

        # create item
        item = Item(
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )
        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in cache
        self.assertIsNone(cache_service.get(object_id))

        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=123,
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

        # now trigger event
        handler = ContentItemFieldUpdateField()
        handler.handle(event)
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cache_service.get(object_id))
        self.assertEquals('Updated body', cached.body)

        # rollback
        handler.rollback(event)

        # assert cache updated
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cached)
        self.assertEquals('Initial body', cached.body)

    def test_update_field_rollback__updates_index(self):
        """ Update field rollback updates index """
        object_id = str(uuid1())
        type = 'plain_text'

        # create item
        item = Item(
            type=type,
            author=123,
            object_id=object_id,
            body='Initial body'
        )
        items = db.tables['items']
        with db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db(update=False))
            item.id = result.inserted_primary_key[0]

        # assert not in index
        self.assertIsNone(search_service.get(type, object_id))

        event = Event(
            id=123,
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=123,
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

        # now trigger event
        handler = ContentItemFieldUpdateField()
        handler.handle(event)
        found = search_service.get(type, object_id)
        self.assertIsNotNone(cache_service.get(object_id))
        self.assertEquals('Updated body', found['_source']['body'])

        # rollback
        handler.rollback(event)

        # assert cache updated
        found = search_service.get(type, object_id)
        self.assertIsNotNone(found)
        self.assertEquals('Initial body', found['_source']['body'])
