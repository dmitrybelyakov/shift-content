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
            index_name='content_tests'
        )

    def tearDown(self):
        """ Clean up """
        search_service.drop_index()
        search_service.disconnect()
        super().tearDown()

    def test_create_search_service(self):
        """ Creating search service"""
        service = SearchService(hosts=['elasticsearch:9200'])
        self.assertIsInstance(service, SearchService)

    def test_can_access_elasticsearch_instance(self):
        """ Create and access elasticsearch instance"""
        service = search_service
        es = service.es
        self.assertIsInstance(es, Elasticsearch)

    def test_get_index_config(self):
        """ Getting index config """
        service = search_service
        index = service.get_index_config()
        self.assertTrue(type(index) is dict)
        self.assertEquals(index['index'], service.index_name)

    def test_get_index_info(self):
        """ Getting index info """
        service = search_service
        info = service.index_info
        self.assertTrue(type(info) is dict)

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

        # delete first
        search_service.es.indices.delete(
            search_service.index_name,
            ignore=404
        )

        # put to index
        object_id = str(uuid1())
        item = Item(
            id=123,
            type='plain_text',
            object_id=object_id,
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)
        info = search_service.es.indices.get(search_service.index_name)
        self.assertIn(search_service.index_name, info)

    def test_can_index_item(self):
        """ Putting item to index """
        # put to index
        object_id = str(uuid1())
        item = Item(
            id=123,
            type='plain_text',
            object_id=object_id,
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)
        item = search_service.get(object_id)
        self.assertIsNotNone(item)
        self.assertEquals(object_id, item['_id'])

    def test_subsequent_indexing_reindexes(self):
        """ Subsequent calls to index don't result in multiple documents """
        object_id = str(uuid1())
        item = Item(
            id=123,
            type='plain_text',
            object_id=object_id,
            author=123,
            body='Here is some body content'
        )

        search_service.put_to_index(item)
        search_service.put_to_index(item)

        time.sleep(2)  # give it some time
        es = search_service.es
        result = es.search(
            index=search_service.index_name,
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
