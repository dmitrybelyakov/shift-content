from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from uuid import uuid1
from shiftevent.event import Event
from shiftcontent.item import Item
from shiftcontent import cache_service
from shiftcontent import search_service
from shiftcontent import db
from shiftcontent.event_handlers import ContentItemSetParent


@attr('event', 'handler', 'content_item_set_parent')
class ContentItemCacheTest(BaseTestCase):

    def setUp(self):
        cache_service.init()
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        super().setUp()

    def tearDown(self):
        cache_service.delete_all()
        cache_service.disconnect()
        search_service.drop_all_indices()
        search_service.disconnect()
        super().tearDown()

    # --------------------------------------------------------------------------
    # tests
    # --------------------------------------------------------------------------

    def test_instantiating_handler(self):
        """ Instantiating content item set parent handler """
        handler = ContentItemSetParent()
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
        handler = ContentItemSetParent()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child.object_id,
            payload=dict(parent_object_id=parent.object_id),
            payload_rollback=dict(parent_object_id=None)
        ))

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child.object_id)
            result = conn.execute(query).fetchone()
            child = Item().from_db(result)

        # assert parent was set
        self.assertEquals(str(parent.object_id), child.path)

    def test_rollback_event(self):
        """ Handler content item set parent rollback changes """
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
        handler = ContentItemSetParent()
        handler.handle(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child.object_id,
            payload=dict(parent_object_id=parent.object_id),
            payload_rollback=dict(parent_object_id=None)
        ))

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child.object_id)
            result = conn.execute(query).fetchone()
            child = Item().from_db(result)

        # assert parent was set
        self.assertEquals(str(parent.object_id), child.path)

        # rollback now
        handler.rollback(Event(
            id=123,
            type='CONTENT_ITEM_SET_PARENT',
            author=123,
            object_id=child.object_id,
            payload=dict(parent_object_id=parent.id),
            payload_rollback=dict(parent_object_id=None)
        ))

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child.object_id)
            result = conn.execute(query).fetchone()
            child = Item().from_db(result)

        # assert rolled back to none
        self.assertIsNone(child.path)

    def test_setting_parent(self):
        """ Setting parent on content item """
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
        handler = ContentItemSetParent()
        handler.set_parent(
            item_object_id=child.object_id,
            parent_object_id=parent.object_id
        )

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child.object_id)
            result = conn.execute(query).fetchone()
            child = Item().from_db(result)

        # assert parent was set
        self.assertEquals(str(parent.object_id), child.path)

    def test_setting_parent_to_none(self):
        """ Setting item parent to none (move item to root) """
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
            body='I am a parent2'
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
            parent.set_field(
                'id', result.inserted_primary_key[0], initial=True
            )

        # set parents now
        handler = ContentItemSetParent()
        handler.set_parent(
            item_object_id=child3.object_id,
            parent_object_id=child2.object_id
        )
        handler.set_parent(
            item_object_id=child2.object_id,
            parent_object_id=child1.object_id
        )
        handler.set_parent(
            item_object_id=child1.object_id,
            parent_object_id=parent.object_id
        )

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

        self.assertEquals(
            '{}.{}.{}'.format(
                parent.object_id, child1.object_id, child2.object_id
            ),
            child3.path
        )

        # now set parent to None
        handler.set_parent(
            item_object_id=child1.object_id,
            parent_object_id=None
        )

        # now get back
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == child1.object_id)
            result = conn.execute(query).fetchone()
            child1 = Item().from_db(result)

            query = items.select().where(items.c.object_id == child3.object_id)
            result = conn.execute(query).fetchone()
            child3 = Item().from_db(result)

        self.assertIsNone(child1.path)
        self.assertEquals('{}.{}'.format(
            child1.object_id, child2.object_id),
            child3.path
        )

    def test_setting_parent_updates_children(self):
        """ Setting item parent updates children """
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

        parent1 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a parent1'
        )

        parent2 = Item(
            type='plain_text',
            author=123,
            object_id=str(uuid1()),
            body='I am a parent2'
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

            result = conn.execute(query, **parent1.to_db(update=False))
            parent1.set_field(
                'id', result.inserted_primary_key[0], initial=True
            )

            result = conn.execute(query, **parent2.to_db(update=False))
            parent2.set_field(
                'id', result.inserted_primary_key[0], initial=True
            )

        # set parents now
        handler = ContentItemSetParent()
        handler.set_parent(
            item_object_id=child3.object_id,
            parent_object_id=child2.object_id
        )
        handler.set_parent(
            item_object_id=child2.object_id,
            parent_object_id=child1.object_id
        )
        handler.set_parent(
            item_object_id=child1.object_id,
            parent_object_id=parent1.object_id
        )

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
            '{}'.format(parent1.object_id),
            child1.path
        )
        self.assertEquals(
            '{}.{}'.format(parent1.object_id, child1.object_id),
            child2.path
        )
        self.assertEquals(
            '{}.{}.{}'.format(
                parent1.object_id, child1.object_id, child2.object_id
            ),
            child3.path
        )

        # now move item (with existing path) to another parent
        handler.set_parent(
            item_object_id=child1.object_id,
            parent_object_id=parent2.object_id
        )

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
            '{}'.format(parent2.object_id),
            child1.path
        )
        self.assertEquals(
            '{}.{}'.format(parent2.object_id, child1.object_id),
            child2.path
        )
        self.assertEquals(
            '{}.{}.{}'.format(
                parent2.object_id, child1.object_id, child2.object_id
            ),
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
        handler = ContentItemSetParent()
        handler.set_parent(
            item_object_id=child2.object_id,
            parent_object_id=child1.object_id
        )
        handler.set_parent(
            item_object_id=child1.object_id,
            parent_object_id=parent.object_id
        )

        # assert items in cache now
        self.assertIsNotNone(cache_service.get(child1.object_id))
        self.assertIsNotNone(cache_service.get(child2.object_id))

    def test_setting_parent_updates_index(self):
        """ Handler content item handle updates index """
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

        # assert not in index (yet)
        self.assertIsNone(search_service.get(child1.type, child1.object_id))
        self.assertIsNone(search_service.get(child2.type, child2.object_id))

        # trigger events
        handler = ContentItemSetParent()
        handler.set_parent(
            item_object_id=child2.object_id,
            parent_object_id=child1.object_id
        )
        handler.set_parent(
            item_object_id=child1.object_id,
            parent_object_id=parent.object_id
        )

        # assert items in index now
        self.assertIsNotNone(search_service.get(child1.type, child1.object_id))
        self.assertIsNotNone(search_service.get(child1.type, child2.object_id))


