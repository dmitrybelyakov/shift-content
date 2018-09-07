from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftcontent import db
from shiftcontent.event_handlers import ContentItemSetParent


@attr('event', 'handler', 'content_item_set_parent')
class ContentItemCacheTest(BaseTestCase):

    def setUp(self):
        cache_service.init()
        super().setUp()

    def tearDown(self):
        cache_service.delete_all()
        cache_service.disconnect()
        super().tearDown()

    # --------------------------------------------------------------------------
    # tests
    # --------------------------------------------------------------------------

    def test_instantiating_handler(self):
        """ Instantiating content item set parent handler """
        handler = ContentItemSetParent(db=self.db)
        self.assertIsInstance(handler, ContentItemSetParent)

    def test_handle_event(self):
        """ Handler content item set parent handles event"""
        # create items
        child = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a child'
        )

        parent = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a parent'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.insert()
            result = conn.execute(query, **child.to_db(update=False))
            child.set_field('id', result.inserted_primary_key[0], initial=True)
            result = conn.execute(query, **parent.to_db(update=False))
            parent.set_field('id', result.inserted_primary_key[0], initial=True)

        # trigger event
        handler = ContentItemSetParent(db=self.db)
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child.object_id,
            payload=dict(parent_id=parent.id),
            payload_rollback=None
        ))

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child.object_id)
            result = conn.execute(query).fetchone()
            child = Item().from_db(result)

        # assert parent was set
        self.assertEquals(str(parent.id), child.path)

    def test_handle_updates_children(self):
        """ Handler content item handle updates children """
        # create items
        child1 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a child1'
        )

        child2 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a child2'
        )

        child3 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a child3'
        )

        parent = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a parent'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.insert()
            result = conn.execute(query, **child1.to_db(update=False))
            child1.set_field('id', result.inserted_primary_key[0], initial=True)

            result = conn.execute(query, **child2.to_db(update=False))
            child2.set_field('id', result.inserted_primary_key[0], initial=True)

            result = conn.execute(query, **child3.to_db(update=False))
            child3.set_field('id', result.inserted_primary_key[0], initial=True)

            result = conn.execute(query, **parent.to_db(update=False))
            parent.set_field('id', result.inserted_primary_key[0], initial=True)

        # trigger events
        handler = ContentItemSetParent(db=self.db)
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child3.object_id,
            payload=dict(parent_id=child2.id),
            payload_rollback=None
        ))
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child2.object_id,
            payload=dict(parent_id=child1.id),
            payload_rollback=None
        ))
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child1.object_id,
            payload=dict(parent_id=parent.id),
            payload_rollback=None
        ))

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child1.object_id)
            result = conn.execute(query).fetchone()
            child1 = Item().from_db(result)

            query = items.select().where(items.c.object_id == child2.object_id)
            result = conn.execute(query).fetchone()
            child2 = Item().from_db(result)

            query = items.select().where(items.c.object_id == child3.object_id)
            result = conn.execute(query).fetchone()
            child3 = Item().from_db(result)

        # assert paths set properly
        self.assertEquals(
            '{}'.format(parent.id),
            child1.path
        )
        self.assertEquals(
            '{}.{}'.format(parent.id, child1.id),
            child2.path
        )
        self.assertEquals(
            '{}.{}.{}'.format(parent.id, child1.id, child2.id),
            child3.path
        )

    def test_setting_parent_updates_cache(self):
        """ Handler content item handle updates cache """
        # create items
        child1 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a child1'
        )

        child2 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a child2'
        )

        parent = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a parent'
        )

        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.insert()
            result = conn.execute(query, **child1.to_db(update=False))
            child1.set_field('id', result.inserted_primary_key[0], initial=True)

            result = conn.execute(query, **child2.to_db(update=False))
            child2.set_field('id', result.inserted_primary_key[0], initial=True)

            result = conn.execute(query, **parent.to_db(update=False))
            parent.set_field('id', result.inserted_primary_key[0], initial=True)

        # assert not in cache (yet)
        self.assertIsNone(cache_service.get(child1.object_id))
        self.assertIsNone(cache_service.get(child2.object_id))

        # trigger events
        handler = ContentItemSetParent(db=self.db)
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child2.object_id,
            payload=dict(parent_id=child1.id),
            payload_rollback=None
        ))
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child1.object_id,
            payload=dict(parent_id=parent.id),
            payload_rollback=None
        ))

        # assert items in cache now
        self.assertIsNotNone(cache_service.get(child1.object_id))
        self.assertIsNotNone(cache_service.get(child2.object_id))

    @attr('zzz')
    def test_setting_parent_updates_index(self):
        """ Handler content item handle updates index """
        self.fail('Implement me!')

    def test_rollback_event(self):
        """ Handler content item set parent rollback changes """
        self.fail('Implement me!')

    def test_rollback_event_updates_children(self):
        """ Handler content item set parent rollback updates children """
        self.fail('Implement me!')

    def test_rollback_event_updates_cache(self):
        """ Handler content item set parent rollback updates cache """
        self.fail('Implement me!')

    def test_rollback_event_updates_index(self):
        """ Handler content item set parent rollback updates index """
        self.fail('Implement me!')


    # def test_handle_event(self):
    #     """ Handler content item cache handles event"""
    #     # create item
    #     object_id = str(uuid1())
    #     item = Item(
    #         type='plain_text',
    #         author=123,
    #         object_id=object_id,
    #         body='Some body content'
    #     )
    #
    #     items = db.tables['items']
    #     with db.engine.begin() as conn:
    #         result = conn.execute(items.insert(), **item.to_db(update=False))
    #         item.id = result.inserted_primary_key[0]
    #
    #     # trigger event
    #     handler = ContentItemCache(db=self.db)
    #     handler.handle(Event(
    #         id=123,
    #         type='CONTENT_ITEM_INDEX',
    #         author=123,
    #         object_id=object_id,
    #         payload=None,
    #         payload_rollback=None
    #     ))
    #
    #     # assert cached
    #     cached = cache_service.get(object_id)
    #     self.assertEquals(item.object_id, cached.object_id)
    #     self.assertEquals(item.body, cached.body)
    #
    # def test_rollback_event(self):
    #     """ Handler content item cache rolling back changes """
    #     # create item
    #     object_id = str(uuid1())
    #     item = Item(
    #         type='plain_text',
    #         author=123,
    #         object_id=object_id,
    #         body='Some body content'
    #     )
    #
    #     items = db.tables['items']
    #     with db.engine.begin() as conn:
    #         result = conn.execute(items.insert(), **item.to_db(update=False))
    #         item.id = result.inserted_primary_key[0]
    #
    #     # trigger event
    #     handler = ContentItemCache(db=self.db)
    #     handler.rollback(Event(
    #         id=123,
    #         type='CONTENT_ITEM_INDEX',
    #         author=123,
    #         object_id=object_id,
    #         payload=None,
    #         payload_rollback=None
    #     ))
    #
    #     # assert cached
    #     cached = cache_service.get(object_id)
    #     self.assertEquals(item.object_id, cached.object_id)
    #     self.assertEquals(item.body, cached.body)
