from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from pprint import pprint as pp
from elasticsearch import Elasticsearch
from shiftcontent import search_service
from shiftcontent.search_service import SearchService
from shiftcontent.item import Item
from shiftcontent import exceptions as x
import time


@attr('search', 'service')
class SearchServiceTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        search_service.init(
            hosts=['127.0.0.1:9200'],
            index_prefix='content_tests'
        )

    def tearDown(self):
        """ Clean up """
        search_service.drop_all_indices()
        search_service.disconnect()
        super().tearDown()

    def test_create_search_service(self):
        """ Creating search service"""
        service = SearchService(hosts=['elasticsearch:9200'])
        self.assertIsInstance(service, SearchService)

    def test_getting_index_name(self):
        """ Prefixing index name with index prefix """
        index_name = 'blog_post'
        result = search_service.index_name(index_name)
        self.assertEquals('content_tests.blog_post', result)

    def test_can_access_elasticsearch_instance(self):
        """ Create and access elasticsearch instance"""
        service = search_service
        es = service.es
        self.assertIsInstance(es, Elasticsearch)

    def test_get_index_config(self):
        """ Getting index config """
        service = search_service
        index = service.get_index_config('blog_post')
        self.assertTrue(type(index) is dict)
        self.assertEquals(index['index'], 'content_tests.blog_post')

    def test_get_index_info(self):
        """ Getting index info """
        index_name = 'blog_post'
        es = search_service.es
        index = es.indices.get(
            'content_tests.' + index_name,
            ignore_unavailable=True
        )
        self.assertFalse(index)

        index = search_service.index_info(index_name)
        self.assertTrue(index)
        self.assertIn('content_tests.' + index_name, search_service.indices)

    def test_deleting_single_index(self):
        """ Deleting single index """
        index_name = 'blog_post'
        es = search_service.es
        search_service.index_info(index_name)
        index = es.indices.get('content_tests.' + index_name, ignore=404)
        self.assertIn('content_tests.' + index_name, index)

        search_service.drop_index(index_name)
        index = es.indices.get('content_tests.' + index_name, ignore=404)
        self.assertIn('error', index)

    def test_deleting_all_indices(self):
        """ Deleting all indices from content namespace """
        es = search_service.es
        es.indices.create(**dict(
            index='not_part_of_content_indexes',
            body=dict(mappings={}, settings={})
        ))

        search_service.index_info('blog1')
        search_service.index_info('blog2')

        index1 = es.indices.get('not_part_of_content_indexes', ignore=404)
        index2 = es.indices.get('content_tests.blog1', ignore=404)
        index3 = es.indices.get('content_tests.blog2', ignore=404)

        self.assertNotIn('error', index1)
        self.assertNotIn('error', index2)
        self.assertNotIn('error', index3)

        search_service.drop_all_indices()

        index1 = es.indices.get('not_part_of_content_indexes', ignore=404)
        index2 = es.indices.get('content_tests.blog1', ignore=404)
        index3 = es.indices.get('content_tests.blog2', ignore=404)

        self.assertNotIn('error', index1)
        self.assertIn('error', index2)
        self.assertIn('error', index3)

        es.indices.delete('not_part_of_content_indexes', ignore=404)

    def test_when_trying_to_index_bad_item(self):
        """ Raise when trying to index something that is not an item """
        with self.assertRaises(x.SearchError) as cm:
            search_service.put_to_index('crap')
        self.assertIn('Item must be of type', str(cm.exception))

    def test_raise_when_indexing_unsaved_item(self):
        """ Raise when trying to index unsaved item """
        item = Item(type='plain_text', author=123)
        with self.assertRaises(x.SearchError) as cm:
            search_service.put_to_index(item)
        self.assertIn(
            'Item must be saved first to be indexed',
            str(cm.exception)
        )

    def test_raise_when_indexing_item_without_object_id(self):
        """ Raise when trying to index item without object id"""
        item = Item(type='plain_text', author=123, id=123)
        with self.assertRaises(x.SearchError) as cm:
            search_service.put_to_index(item)
        self.assertIn(
            'Item must have object_id to be indexed',
            str(cm.exception)
        )

    def test_indexing_item_creates_index_if_not_found(self):
        """ Create index if not found when indexing an item """
        item = Item(
            id=123,
            type='plain_text',
            object_id=str(uuid1()),
            author=123,
            body='Here is some body content'
        )

        # delete first
        index_name = search_service.index_name(item.type)
        search_service.es.indices.delete(index_name, ignore=404)

        # put to index
        search_service.put_to_index(item)
        info = search_service.es.indices.get(index_name)
        self.assertIn(index_name, info)

    def test_can_index_item(self):
        """ Putting item to index """
        item = Item(
            id=123,
            type='plain_text',
            object_id=str(uuid1()),
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)
        found = search_service.get(item.type, item.object_id)
        self.assertIsNotNone(found)
        self.assertEquals(item.object_id, found['_id'])

    def test_subsequent_indexing_reindexes(self):
        """ Subsequent calls to index don't result in multiple documents """
        item = Item(
            id=123,
            type='plain_text',
            object_id=str(uuid1()),
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)

        # reindex
        item.body = 'UPDATED'
        search_service.put_to_index(item)

        time.sleep(2)  # give it some time
        es = search_service.es
        result = es.search(
            index=search_service.index_name(item.type),
            doc_type=search_service.doc_type,
            body={
                'query': {
                    'match': {
                        'object_id': item.object_id
                    }
                }
            },
        )
        self.assertEquals(1, result['hits']['total'])
        self.assertEquals(
            'UPDATED',
            result['hits']['hits'][0]['_source']['body']
        )

    def test_getting_item_by_id(self):
        """ Search service can get item by id """
        item = Item(
            id=123,
            type='plain_text',
            object_id=str(uuid1()),
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)
        time.sleep(1)
        found = search_service.get(item.type, item.object_id)
        self.assertEquals(item.object_id, found['_source']['object_id'])

    def test_getting_nonexistent_item(self):
        """ Getting nonexistent item returns None instead of exception"""
        self.assertIsNone(search_service.get('sometype', 'nonexistent'))


    def test_deleting_item_by_id(self):
        """ Search service can delete item by id """
        item = Item(
            id=123,
            type='plain_text',
            object_id=str(uuid1()),
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)
        time.sleep(1)

        search_service.delete(item.type, item.object_id)
        time.sleep(1)
        self.assertIsNone(search_service.get(item.type, item.object_id))

    def test_deleting_nonexistent_item(self):
        """ Deleting nonexistent item does not trow an exception"""
        result = search_service.delete('nonexistent', 'nonexistent')
        self.assertIsInstance(result, SearchService)
