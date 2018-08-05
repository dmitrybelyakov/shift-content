from shiftmemory import Memory
import json
from shiftcontent.item import Item

# TODO: MUST BE A BETTER WAY TO CONFIGURE CACHE SERVICE
# TODO: SINCE WE ARE WORKING WITH MEMORY INDIRECTLY ANYWAYS
# TODO: BETTER NOT PASS DOWN ADAPTERS AND CACHES


class CacheService(Memory):
    """
    Cache service
    Wraps around shiftmemory to provide additional functionality and easier
    configuration for adapters and caches.
    """

    cache_name = 'content'

    def init(
        self,
        cache_name='content',
        default_ttl=44640,
        host='localhost',
        port=6379,
        db=0,
        **kwargs
    ):
        """
        Delayed initializer
        This overrides initializer from  shiftmemory to provides easier
        configuration. We do not need to supply the whole list of adapters and
        caches since we are only using redis adapter and one cache for content
        items.

        :param cache_name: str, cache name for content items
        :param default_ttl: int, ttl in minutes defaults to a month
        :param host: str, redis host, defaults to localhost
        :param port: int, redis port defaults to 6379
        :param db: int, redis database id to use, defaults to 0
        :param kwargs: additional config params to pass to redis adapter
        :return: shiftcontent.cache_service.CacheService
        """

        self.cache_name = cache_name

        # cache adapters (only using redis)
        adapters = dict(
            redis_adapter=dict(
                type='redis',
                config=dict(
                    host=host,
                    port=port,
                    db=db,
                    **kwargs
                )
            )
        )

        # caches
        caches = dict()
        caches[self.cache_name] = dict(
            adapter='redis_adapter',
            ttl=default_ttl
        )

        # configure memory
        super().init(adapters=adapters, caches=caches)
        return self




    @property
    def cache(self):
        """
        Direct access to cache adapter
        :return:
        """
        return self.get_cache('content')

    def disconnect(self):
        """
        Disconnect
        Erases configured adapters and caches
        :return: shiftcontent.cache_service.CacheService
        """
        self.adapters = {}
        self.caches = {}

    def set(self, item, **kwargs):
        """
        Set
        Adds item to cache or updates item cache
        :param item: shiftcontent.item.Item
        :param kwargs: keyword arguments to pass to cache adapter
        :return: shiftcontent.cache_service.CacheService
        """
        data = item.to_cache()
        self.cache.set(item.object_id, data, **kwargs)

    def get(self, object_id):
        """
        Get
        Retrieves item from cache
        :param object_id: str, object id
        :return:
        """
        data = self.cache.get(object_id)
        if not data:
            return

        data = json.loads(data)
        content_type = data['meta']['type']
        item = Item(type=content_type, **data)
        return item

    def delete(self, object_id, **kwargs):
        """
        Delete
        Removes item from cache
        :param object_id: str, object id
        :param kwargs: keyword arguments to pass to cache adapter
        :return: shiftcontent.cache_service.CacheService
        """
        self.cache.delete(object_id, **kwargs)

    def delete_all(self):
        """
        Delete all
        Removes all caches
        :return: shiftcontent.cache_service.CacheService
        """
        self.cache.delete_all()



