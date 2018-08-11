from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.cache_service import CacheService


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

    def test_return_none_for_cache_if_redis_not_configured(self):
        """ Cache service returns None for cache if no Redis"""
        service = CacheService()
        service.disconnect()
        self.assertIsNone(service.cache)

    def test_return_none_when_getting_item_if_no_redis(self):
        """ Cache servcie returns none for an item if no Redis"""
        service = CacheService()
        service.disconnect()
        self.assertIsNone(service.get('something'))

    def test_return_none_when_deleting_item_if_no_redis(self):
        """ Cache servcie returns none when deleting item if no Redis"""
        service = CacheService()
        service.disconnect()
        self.assertIsNone(service.delete('something'))

    def test_return_none_when_deleting_all_if_no_redis(self):
        """ Cache servcie returns none when deleting all if no Redis"""
        service = CacheService()
        service.disconnect()
        self.assertIsNone(service.delete_all())


