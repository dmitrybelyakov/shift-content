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
        adapters = dict(
            redis_adapter=dict(
                adapter='redis',
                config=dict()
            )
        )

        caches = dict(
            demo_cache=dict(
                adapter='redis_adapter',
                ttl=20
            )
        )

        service = CacheService(adapters=adapters, caches=caches)
        self.assertEquals(adapters, service.adapters)
        self.assertEquals(caches, service.caches)

    def test_disconnecting_from_cache(self):
        """ Disconnecting from cache and erasing adapters and caches """
        adapters = dict(
            redis_adapter=dict(
                adapter='redis',
                config=dict()
            )
        )

        caches = dict(
            demo_cache=dict(
                adapter='redis_adapter',
                ttl=20
            )
        )

        service = CacheService(adapters=adapters, caches=caches)
        service.disconnect()
        self.assertFalse(service.adapters)
        self.assertFalse(service.caches)
