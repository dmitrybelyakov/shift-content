from shiftmemory import Memory
import json
from shiftcontent.item import Item

class CacheService(Memory):
    """
    Cache service
    Extends cache service from shiftmemory to provide convenience methods
    to disconnect from cache. Mostly used during testing
    """

    cache_name = 'content'

    @property
    def cache(self):
        """
        Direct access to cache adapter
        :return:
        """
        return self.get_cache(self.cache_name)

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



