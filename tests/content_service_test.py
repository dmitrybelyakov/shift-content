from tests.base import BaseTestCase
from nose.plugins.attrib import attr
from pprint import pprint as pp

from uuid import uuid1
from datetime import datetime
from shiftschema.schema import Result, Schema
from shiftcontent import db
from shiftcontent import content_service
from shiftcontent import exceptions as x
from shiftcontent.content_service import ContentService
from shiftcontent.item import Item
from shiftcontent.item_schema import UpdateItemSchema, CreateItemSchema
from shiftcontent import search_service
from shiftcontent import cache_service
from shiftmemory import exceptions as cx
import time


@attr('content', 'service')
class ContentServiceTest(BaseTestCase):

    def setUp(self):
        cache_service.init()
        super().setUp()

    def tearDown(self):
        try:
            cache_service.delete_all()
            cache_service.disconnect()
        except cx.ConfigurationException:
            pass

        super().tearDown()

    # --------------------------------------------------------------------------
    # tests
    # --------------------------------------------------------------------------

    def test_create_content_service(self):
        """ Creating content service"""
        service = ContentService()
        self.assertIsInstance(service, ContentService)

    def test_creating_item_update_schema(self):
        """ Create schema for content item update """
        schema = content_service.item_schema('plain_text', 'update')
        self.assertIsInstance(schema, UpdateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_creating_item_create_schema(self):
        """ Create schema for content item creation """
        schema = content_service.item_schema('plain_text', 'create')
        self.assertIsInstance(schema, CreateItemSchema)

        # assert custom filters and validators added to prop
        self.assertIn('body', schema.properties)
        prop = getattr(schema, 'body')
        self.assertEquals(1, len(prop.filters))
        self.assertEquals(2, len(prop.validators))

    def test_raise_on_requesting_bad_schema_type(self):
        """ Item schema type can be either create or update """
        with self.assertRaises(x.InvalidItemSchemaType):
            content_service.item_schema('plain_text', 'BAD')

    def test_get_item(self):
        """ Getting item by object id """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created= datetime.utcnow(),
            object_id=object_id,
            type='plain_text',
            fields='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        item = content_service.get_item(object_id=object_id)
        self.assertIsInstance(item, Item)

    def test_getting_item_puts_it_to_cache(self):
        """ Getting content item pts it to cache """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created=datetime.utcnow(),
            object_id=object_id,
            type='plain_text',
            fields='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        content_service.get_item(object_id)

        # assert put in cache
        cached = cache_service.get(object_id)
        self.assertIsNotNone(cached)

    def test_skip_putting_to_cache_if_not_configured(self):
        """ Content service skips putting item to cache if not configured """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created= datetime.utcnow(),
            object_id=object_id,
            type='plain_text',
            fields='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        cache_service.disconnect()
        item = content_service.get_item(object_id)
        self.assertIsNotNone(item)

    def test_getting_item_from_cache(self):
        """ Getting item from cache"""
        object_id = str(uuid1())
        data = dict(
            author=123,
            created= datetime.utcnow(),
            object_id=object_id,
            type='plain_text',
            fields='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        item = content_service.get_item(object_id)

        # modify what's in cache
        new_value = 'UPDATED'
        item.body = new_value
        cache_service.set(item)

        # now get from content service
        cached = content_service.get_item(object_id)
        self.assertEquals(new_value, cached.body)

    def test_fail_to_initialize_an_item_from_database_if_type_is_unknown(self):
        """ Fail to initialize item from database if type not in schema """
        object_id = str(uuid1())
        data = dict(
            author=123,
            created=datetime.utcnow(),
            object_id=object_id,
            type='nonexistent',
            data='{"body": "some content"}'
        )

        # insert
        items = db.tables['items']
        with db.engine.begin() as conn:
            conn.execute(items.insert(), **data)

        # now get it
        with self.assertRaises(x.UndefinedContentType) as cm:
            content_service.get_item(object_id=object_id)
        err = 'Database contains item (1) of undefined type [nonexistent]'
        self.assertIn(err, str(cm.exception))

    # --------------------------------------------------------------------------
    # CRUD & events
    # --------------------------------------------------------------------------

    def test_create_content_item(self):
        """ Create a simple content item """
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item 😂😂😂😂')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        self.assertEquals(1, item.id)

    def test_getting_item_schema(self):
        """ Generating filtering and validation for an item by type """
        schema1 = content_service.item_schema('plain_text')
        self.assertIsInstance(schema1, Schema)

        schema2 = content_service.item_schema('markdown')
        self.assertIsInstance(schema2, Schema)

        # assert no extra props added
        meta = ['id', 'author', 'type', 'object_id']
        for prop, prop_obj in schema2.properties.items():
            self.assertIn(prop, meta)

    def test_created_item_filtered(self):
        """ Incoming data is filtered with schema when creeating item """
        type = 'plain_text'
        author = 123
        fields = dict(body='   I am a simple content item   ')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )
        self.assertEquals('I am a simple content item', item.body)

    def test_return_validation_result_when_creating_with_invalid_data(self):
        """ Return validation errors when creating item with bad data """
        type = 'plain_text'
        author = 123
        fields = dict(body='')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )
        self.assertIsInstance(item, Result)
        err = item.get_messages()
        self.assertIn('body', err)
        self.assertEquals(2, len(err['body']))

    def test_raise_when_creating_an_item_of_undefined_type(self):
        """ Raise when creating content item of undefined type """
        with self.assertRaises(x.UndefinedContentType):
            content_service.create_item(
                author='123',
                content_type='BAD!',
                fields={}
            )

    def test_raise_on_deleting_nonexistent_item(self):
        """ Raise when attempting to delete nonexistent item """
        with self.assertRaises(x.ItemNotFound) as cm:
            content_service.delete_item(123, 123)
        self.assertIn(
            'Unable to delete nonexistent content item',
            str(cm.exception)
        )

    def test_deleting_content_item(self):
        """ Deleting content item """
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )
        object_id = item.object_id
        content_service.delete_item(author, item.object_id)

        with self.db.engine.begin() as conn:
            items = self.db.tables['items']
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            self.assertIsNone(result)

    def test_raise_when_updating_item_of_bad_type(self):
        """ Fail to update item of bad type """
        with self.assertRaises(x.ItemError) as cm:
            content_service.update_item(author='12345', item=dict())
        self.assertIn('Update function expects', str(cm.exception))

    def test_raise_on_updating_nonexistent_item(self):
        """ test when trying to update nonexistent item """
        with self.assertRaises(x.ItemNotFound) as cm:
            item = Item(type='plain_text', author=123, body='I am a body')
            content_service.update_item(author=123, item=item)
        self.assertIn('Item must be saved first', str(cm.exception))

    def test_updating_content_item(self):
        """ Updating content item """
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        item.body = 'I am updated body'
        updated = content_service.update_item(author, item)
        self.assertEquals('I am updated body', updated.body)

    def test_return_validation_errors_if_updating_with_invalid_data(self):
        """ Validate data when updating content item """
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        item.body = '0'
        result = content_service.update_item(author, item)
        self.assertIsInstance(result, Result)
        self.assertFalse(result)
        self.assertIn('body', result.get_messages())

    def test_raise_on_updating_filed_for_nonexistent_item(self):
        """ Raise error when updating field on nonexistent item """
        with self.assertRaises(x.ItemNotFound) as cm:
            content_service.update_item_field(1, 'NONEXISTENT', 'body', '')
        self.assertIn('Unable to find item with such id', str(cm.exception))

    def test_raise_when_trying_to_update_nonexistent_field(self):
        """ Raise when updating nonexistent field on an item """
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )
        with self.assertRaises(x.ItemError) as cm:
            content_service.update_item_field(author, item.object_id, 'z', '')

        self.assertIn('is not allowed for content type', str(cm.exception))

    def test_return_errors_when_updating_item_field_with_bad_data(self):
        """ Validate data when updating item field"""
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        new_value = '0'
        result = content_service.update_item_field(
            author,
            item.object_id,
            'body',
            new_value
        )

        self.assertIsInstance(result, Result)
        self.assertFalse(result)
        self.assertIn('body', result.get_messages())

    def test_updating_content_item_field(self):
        """ Updating single field on content item """
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        new_value = 'NEW BODY VALUE'
        updated = content_service.update_item_field(
            author,
            item.object_id,
            'body',
            new_value
        )

        self.assertEquals(new_value, updated.body)

    def test_creating_content_item_puts_it_to_index(self):
        """ Creating content item puts it to index"""
        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )
        search_service.drop_index()

        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        time.sleep(2)  # give it some time
        es = search_service.es
        result = es.search(
            index=search_service.index_name,
            doc_type=search_service.doc_type,
            body={
                'query': {
                    # 'match_all': {}
                    'match': {
                        'object_id': item.object_id
                    }
                }
            },
        )

        self.assertEquals(1, result['hits']['total'])
        self.assertEquals(
            item.object_id,
            result['hits']['hits'][0]['_source']['object_id']
        )

        # cleanup
        search_service.drop_index()
        search_service.disconnect()

    def test_updating_content_item_updates_index(self):
        """ Updating content item updates index """
        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        # create first
        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        # then update
        item.body = 'I am updated body'
        content_service.update_item(author, item)

        time.sleep(2)  # give it some time
        es = search_service.es
        result = es.search(
            index=search_service.index_name,
            doc_type=search_service.doc_type,
            body={
                'query': {
                    # 'match_all': {}
                    'match': {
                        'object_id': item.object_id
                    }
                }
            },
        )

        self.assertEquals(
            'I am updated body',
            result['hits']['hits'][0]['_source']['body']
        )

        # cleanup
        search_service.drop_index()
        search_service.disconnect()

    def test_updating_content_item_field_updates_index(self):
        """ Updating content item field updates index """
        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        new_value = 'NEW BODY VALUE'
        content_service.update_item_field(
            author,
            item.object_id,
            'body',
            new_value
        )

        time.sleep(2)  # give it some time
        es = search_service.es
        result = es.search(
            index=search_service.index_name,
            doc_type=search_service.doc_type,
            body={
                'query': {
                    # 'match_all': {}
                    'match': {
                        'object_id': item.object_id
                    }
                }
            },
        )

        self.assertEquals(
            new_value,
            result['hits']['hits'][0]['_source']['body']
        )

        # cleanup
        search_service.drop_index()
        search_service.disconnect()

    def test_deleting_content_item_removes_it_from_index(self):
        """ Deleting content item removes it from index """

        # init search
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_name='content_tests'
        )

        type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=type,
            fields=fields
        )

        object_id = item.object_id
        content_service.delete_item(author, item.object_id)

        time.sleep(2)  # give it some time
        es = search_service.es
        result = es.search(
            index=search_service.index_name,
            doc_type=search_service.doc_type,
            body={
                'query': {
                    # 'match_all': {}
                    'match': {
                        'object_id': object_id
                    }
                }
            },
        )

        self.assertEquals(0, result['hits']['total'])

        # cleanup
        search_service.drop_index()
        search_service.disconnect()

    def test_creating_content_item_puts_it_to_cache(self):
        """ Creating content item puts it to cache """
        # create item
        content_type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=content_type,
            fields=fields
        )

        cached = cache_service.get(item.object_id)
        self.assertEquals(item.body, cached.body)

    def test_updating_content_item_updates_cache(self):
        """ Updating content item updates cache """
        # create item
        content_type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=content_type,
            fields=fields
        )

        # then update
        item.body = 'I am updated body'
        content_service.update_item(author, item)

        cached = cache_service.get(item.object_id)
        self.assertEquals('I am updated body', cached.body)

    def test_updating_content_item_field_updates_cache(self):
        """ Updating content item field updates cache """
        # create item
        content_type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=content_type,
            fields=fields
        )

        # update field
        new_value = 'NEW BODY VALUE'
        content_service.update_item_field(
            author,
            item.object_id,
            'body',
            new_value
        )

        cached = cache_service.get(item.object_id)
        self.assertEquals(new_value, cached.body)

    def test_deleting_content_item_removes_it_from_cache(self):
        """ Deleting content item removes it from cache """
        # create item
        content_type = 'plain_text'
        author = 123
        fields = dict(body='I am a simple content item')
        item = content_service.create_item(
            author=author,
            content_type=content_type,
            fields=fields
        )

        # and delete
        object_id = item.object_id
        content_service.delete_item(author=author, object_id=object_id)

        cached = cache_service.get(item.object_id)
        self.assertIsNone(cached)

    # --------------------------------------------------------------------------
    # Trees & nesting
    # --------------------------------------------------------------------------

    def test_raise_when_setting_parent_with_no_id(self):
        """ Item must have an id to be a parent """
        item = Item()
        item.set_field('id', 123, initial=True)
        parent = Item()
        author = 123
        with self.assertRaises(x.ItemError) as cm:
            content_service.set_parent(author, item, parent)

        self.assertIn(
            'Item must be saved first to become a parent',
            str(cm.exception)
        )

    def test_raise_when_setting_parent_on_item_with_no_id(self):
        """ Item must have an id to get a parent """
        item = Item()
        parent = Item()
        parent.set_field('id', 123, initial=True)
        author = 123
        with self.assertRaises(x.ItemError) as cm:
            content_service.set_parent(author, item, parent)

        self.assertIn(
            'Item must be saved first to get a parent',
            str(cm.exception)
        )

    def test_raise_when_setting_item_as_parent_of_itself(self):
        """ Forbid to set item as itself's parent """
        item = Item()
        item.set_field('id', 123, initial=True)
        with self.assertRaises(x.ItemError) as cm:
            content_service.set_parent(123, item, item)

        self.assertIn(
            'Unable to set item as a parent of itself',
            str(cm.exception)
        )

    def test_raise_when_setting_item_as_child_of_its_children(self):
        """ Forbid to set parent as child of its children """
        author = 123
        item1 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 1')
        )

        item2 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 2')
        )

        item3 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 3')
        )

        content_service.set_parent(author, item2, item1)
        content_service.set_parent(author, item3, item2)
        with self.assertRaises(x.ItemError) as cm:
            content_service.set_parent(author, item1, item3)

        self.assertIn(
            'Unable to set parent as a child of its children',
            str(cm.exception)
        )

    def test_setting_parent(self):
        """ Setting item parent """
        author = 123
        item1 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 1')
        )

        item2 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 2')
        )

        item3 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 3')
        )

        item4 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child 4')
        )

        parent = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a parent')
        )

        root = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am the root of everything')
        )

        content_service.set_parent(author, item4, item3)
        content_service.set_parent(author, item3, item2)
        content_service.set_parent(author, item2, item1)
        content_service.set_parent(author, item1, parent)
        content_service.set_parent(author, parent, root)

        item1 = content_service.get_item(item1.object_id)
        item2 = content_service.get_item(item2.object_id)
        item3 = content_service.get_item(item3.object_id)
        item4 = content_service.get_item(item4.object_id)
        parent = content_service.get_item(parent.object_id)
        root = content_service.get_item(root.object_id)

        self.assertEquals(None, root.path)
        self.assertEquals(root.object_id, parent.path)
        self.assertEquals(
            '{}.{}'.format(root.object_id, parent.object_id),
            item1.path
        )
        self.assertEquals(
            '{}.{}.{}'.format(
                root.object_id,
                parent.object_id,
                item1.object_id
            ),
            item2.path
        )
        self.assertEquals(
            '{}.{}.{}.{}'.format(
                root.object_id,
                parent.object_id,
                item1.object_id,
                item2.object_id,
            ),
            item3.path
        )
        self.assertEquals(
            '{}.{}.{}.{}.{}'.format(
                root.object_id,
                parent.object_id,
                item1.object_id,
                item2.object_id,
                item3.object_id,
            ),
            item4.path
        )

    def test_set_parent_when_creating_an_item(self):
        """ Set parent when creating an item """
        author = 123
        parent = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a parent')
        )

        item = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child'),
            parent=parent
        )

        self.assertEquals(str(parent.object_id), item.path)

    def test_getting_item_path(self):
        """ Getting item path """
        author = 123
        item = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a child')
        )

        parent = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a parent')
        )

        root = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am the root of everything')
        )

        content_service.set_parent(author, item, parent)
        content_service.set_parent(author, parent, root)

        path = content_service.get_path(item.object_id)
        self.assertTrue(type(path) is list)
        self.assertEquals(root.object_id, path[0].object_id)
        self.assertEquals(parent.object_id, path[1].object_id)

    def test_getting_item_children(self):
        """ Getting item children """
        author = 123
        child1 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am child 1')
        )
        child2 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am child 2')
        )

        child3 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am child 3')
        )

        parent = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a parent')
        )

        content_service.set_parent(author, child1, parent)
        content_service.set_parent(author, child2, parent)
        content_service.set_parent(author, child3, child2)

        children = content_service.get_children(parent.object_id)
        ids = [child.object_id for child in children]

        self.assertIn(child1.object_id, ids)
        self.assertIn(child2.object_id, ids)
        self.assertNotIn(child3.object_id, ids)

    def test_getting_tem_descendants(self):
        """ Getting item descendants """
        author = 123
        child1 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am child 1')
        )
        child2 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am child 2')
        )

        child3 = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am child 3')
        )

        parent = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am a parent')
        )

        root = content_service.create_item(
            author=author,
            content_type='plain_text',
            fields=dict(body='I am the root element')
        )

        content_service.set_parent(author, parent, root)
        content_service.set_parent(author, child1, parent)
        content_service.set_parent(author, child2, child1)
        content_service.set_parent(author, child3, child2)

        descendants = content_service.get_descendants(parent.object_id)
        ids = [descendant.object_id for descendant in descendants]

        self.assertIn(child1.object_id, ids)
        self.assertIn(child2.object_id, ids)
        self.assertIn(child3.object_id, ids)

        self.assertNotIn(parent.object_id, ids)
        self.assertNotIn(root.object_id, ids)

    # @attr('zzz')
    # def test_getting_tree(self):
    #     """ Getting item tree """
    #     author = 123
    #     child1 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am child 1')
    #     )
    #     child2 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am child 2')
    #     )
    #
    #     child3 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am child 3')
    #     )
    #     child4 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am child 4')
    #     )
    #     child5 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am child 5')
    #     )
    #
    #     child6 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am child 6')
    #     )
    #
    #     parent1 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am parent 1')
    #     )
    #
    #     parent2 = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am parent 2')
    #     )
    #
    #     root = content_service.create_item(
    #         author=author,
    #         content_type='plain_text',
    #         fields=dict(body='I am a root element')
    #     )
    #
    #     # branch 1
    #     content_service.set_parent(author, parent1, root)
    #     content_service.set_parent(author, child1, parent1)
    #     content_service.set_parent(author, child2, child1)
    #     content_service.set_parent(author, child3, child2)
    #
    #     # branch 2
    #     content_service.set_parent(author, parent2, root)
    #     content_service.set_parent(author, child4, parent2)
    #     content_service.set_parent(author, child5, child4)
    #     content_service.set_parent(author, child6, child5)
    #
    #     tree = content_service.get_tree()
    #     self.fail('Implement me!')
