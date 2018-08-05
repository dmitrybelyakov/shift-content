from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from uuid import uuid1
from pprint import pprint as pp
from elasticsearch import Elasticsearch
from shiftcontent import search_service
from shiftcontent.cache_service import CacheService
from shiftcontent.item import Item
from shiftcontent import exceptions as x
import time


@attr('cache', 'service')
class CacheServiceTest(BaseTestCase):

    def test_create_search_service(self):
        """ Creating search service"""
        service = CacheService()
        self.assertIsInstance(service, CacheService)

    def test_delayed_init_cache(self):
        """ Using delayed cache initialization """
        cfg = dict(
            cache_name='updated_content',
            default_ttl=30,
            host='127.0.0.1',
            port=6379,
            db=1
        )
        service = CacheService()
        service.init(**cfg)

        adapters = service.adapters
        caches = service.caches

        self.assertIn('redis_adapter', adapters)
        self.assertEquals(
            cfg['host'],
            adapters['redis_adapter']['config']['host']
        )
        self.assertEquals(
            cfg['port'],
            adapters['redis_adapter']['config']['port']
        )
        self.assertEquals(
            cfg['db'],
            adapters['redis_adapter']['config']['db']
        )

        self.assertIn('updated_content', caches)
        self.assertEquals(30, caches['updated_content']['ttl'])

    def test_disconnecting_from_cache(self):
        """ Disconnecting from cache and erasing adapters and caches """
        service = CacheService(host='localhost', port=6379)
        service.disconnect()
        self.assertFalse(service.adapters)
        self.assertFalse(service.caches)
