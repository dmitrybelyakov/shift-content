from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import exceptions as ex
from pprint import pprint as pp

from shiftcontent.item import Item
from shiftcontent import definition_service
from shiftcontent import exceptions as x


class SearchService:

    def __init__(self, *_, **kwargs):
        """
        Init service
        If any kwargs are given to constructor, a delayed initializer is
        called with these kwargs. This class only accepts kwargs.
        """

        # es connection [host:port]
        self.hosts = ()

        # es instance
        self._es = None

        # index name
        self.index_name = None

        # document type
        self.doc_type = None

        self.sniff = True

        if kwargs:
            self.init(**kwargs)

    def init(
        self,
        *,
        hosts=('localhost:9002',),
        index_name=None,
        doc_type='content',
        sniff=True):
        """
        Delayed service initializer. Called either by constructor if args
        passed in, or later in userland code to configure the service.

        :param hosts: iterable, hosts (and ports) to connect to
        :param port: int, elasticsearch port
        :param index_name: str, index name
        :param doc_type: str, document type
        :param sniff: bool, whether to sniff on start
        :return: shiftcontent.search_service.SearchService
        """
        self.hosts = hosts
        self.index_name = index_name
        self.doc_type = doc_type
        self.sniff = sniff
        return self

    @property
    def es(self):
        """
        Elasticsearch instance
        :return:
        """
        if not self._es:
            self._es = Elasticsearch(self.hosts, sniff_on_start=self.sniff)
        return self._es

    @property
    def index_info(self):
        """
        Index info
        Returns information about te index and creates one if not found.
        :return:
        """
        try:
            index = self.es.indices.get(self.index_name)
        except ex.NotFoundError:
            self.es.indices.create(**self.get_index_config())
            index = self.es.indices.get(self.index_name)

        return index

    def disconnect(self):
        """
        Disconnect
        Erase credentials and drop the client. This is mostly used in testing
        environment.
        :return: shiftcontent.search_service.SearchService
        """
        self.hosts = ()
        self._es = None
        return self

    def drop_index(self):
        """
        Drop index
        Deletes index and all the documents in it.
        :return: shiftcontent.search_service.SearchService
        """
        self.es.indices.delete(self.index_name, ignore=404)
        return self

    def get_index_config(self):
        """
        Get index config
        Returns index config based off content definition
        :return: dict
        """
        config = {
            'index': self.index_name,
            'body': {
                'mappings': {},
                'settings': {}
            }
        }

        return config

    def get(self, object_id):
        """
        Get single item from index by its object id
        :param object_id: str, object id
        :return:
        """
        try:
            item = self.es.get(
                index=self.index_name,
                doc_type=self.doc_type,
                id=object_id,
            )
        except ex.NotFoundError:
            return None

        return item

    def delete(self, object_id):
        """
        Delete
        Removes item from index by object_id
        :param object_id: str, object id
        :return: shiftcontent.search_service
        """
        self.es.delete(
            index=self.index_name,
            doc_type=self.doc_type,
            id=object_id
        )

        return self

    def put_to_index(self, item):
        """
        Put item to index
        Gets pickeled representation of item and puts it to index
        :param item:
        :return:
        """
        if not isinstance(item, Item):
            err = 'Item must be of type shiftcontent.item.Item to be indexed.' \
                  ' Got {} instead'
            raise x.SearchError(err.format(type(item)))

        if not item.id:
            raise x.SearchError('Item must be saved first to be indexed')

        if not item.object_id:
            raise x.SearchError('Item must have object_id to be indexed')

        # create index if required
        self.index_info

        indexable = item.to_search()
        self.es.index(
            index=self.index_name,
            doc_type=self.doc_type,
            id=item.object_id,
            body=indexable
        )








