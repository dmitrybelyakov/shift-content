from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from elasticsearch import Elasticsearch
from shiftcontent import search_service
from shiftcontent.search_service import SearchService


@attr('search', 'service')
class SearchServiceTest(BaseTestCase):

    def tearDown(self):
        """ Drop index"""
        search_service.es.indices.delete(
            search_service.index_name,
            ignore=404
        )
        super().tearDown()

    def test_create_search_service(self):
        """ Creating search service"""
        service = SearchService()
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


