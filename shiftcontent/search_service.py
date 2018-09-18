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

        # index prefix
        self.index_prefix = None

        # index data collection
        self.indices = dict()

        # document type
        self.doc_type = None

        # sniff nodes
        self.sniff = True

        # additional params
        self.additional_params = dict()

        if kwargs:
            self.init(**kwargs)

    def init(
        self,
        *,
        hosts=('localhost:9002',),
        index_prefix=None,
        doc_type='content',
        sniff=True,
        **kwargs):
        """
        Delayed service initializer. Called either by constructor if args
        passed in, or later in userland code to configure the service.

        :param hosts: iterable, hosts (and ports) to connect to
        :param port: int, elasticsearch port
        :param index_prefix: str, prefix to add to index names (per type)
        :param doc_type: str, document type
        :param sniff: bool, whether to sniff on start
        :param kwargs: dict, additional parameters to pass to elasticsearch
        :return: shiftcontent.search_service.SearchService
        """
        self.hosts = hosts
        self.index_prefix = index_prefix
        self.doc_type = doc_type
        self.sniff = sniff
        self.additional_params = kwargs
        return self

    @property
    def es(self):
        """
        Elasticsearch instance
        :return:
        """
        if not self._es:
            self._es = Elasticsearch(
                self.hosts,
                sniff_on_start=self.sniff,
                **self.additional_params
            )
        return self._es

    def index_name(self, index_name):
        """
        Index name
        Prefixes index name with index prefix if configured
        :param index_name: str, index name
        :return: str
        """
        if self.index_prefix:
            index_name = '{}.{}'.format(self.index_prefix, index_name)

        return index_name

    def index_info(self, index_name):
        """
        Index info
        Returns information about te index and creates one if not found.

        :param index_name: str, index name
        :return: dict
        """
        full_index_name = self.index_name(index_name)
        if index_name not in self.indices.keys():
            try:
                index = self.es.indices.get(full_index_name)
            except ex.NotFoundError:
                self.es.indices.create(**self.get_index_config(index_name))
                index = self.es.indices.get(full_index_name)

            self.indices[full_index_name] = index

        return self.indices[full_index_name]

    def disconnect(self):
        """
        Disconnect
        Erase credentials and drop the client. This is mostly used in testing
        environment.
        :return: shiftcontent.search_service.SearchService
        """
        self.hosts = ()
        self._es = None
        self.index_prefix = None
        self.indices = dict()
        return self

    def drop_index(self, index_name):
        """
        Drop index
        Deletes index and all the documents in it.

        :param index_name: str, index name
        :return: shiftcontent.search_service.SearchService
        """
        self.es.indices.delete(self.index_name(index_name), ignore=404)
        return self

    def drop_all_indices(self):
        """
        Drop all indices
        Removes all indices and data under self.index_prefix namespace if
        configures, otherwise removes everything in elasticsearch.
        :return: shiftcontent.search_service.SearchService
        """
        self.es.indices.delete('{}*'.format(self.index_prefix), ignore=404)
        return self

    def get_index_config(self, index_name):
        """
        Get index config
        Returns index config based off content definition

        :param index_name: str, index name
        :return: dict
        """
        index_name = self.index_name(index_name)

        config = {
            'index': index_name,
            'body': {
                'mappings': {},
                'settings': {}
            }
        }

        return config

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

        try:
            # create index if required
            index_name = self.index_name(item.type)
            if index_name not in self.indices:
                self.index_info(item.type)

            # put to index
            self.es.index(
                index=index_name,
                doc_type=self.doc_type,
                id=item.object_id,
                body=item.to_search()
            )
        except ex.ImproperlyConfigured:
            pass

        return self

    def get(self, index_name, object_id):
        """
        Get single item from index by its object id
        :param index_name: str, index name
        :param object_id:
        :return:
        """
        try:
            item = self.es.get(
                index=self.index_name(index_name),
                doc_type=self.doc_type,
                id=object_id,
            )
        except ex.NotFoundError:
            return None
        except ex.ImproperlyConfigured:
            return None

        return item

    def delete(self, index_name, object_id):
        """
        Delete
        Removes item from index by object_id

        :param index_name: str, index name
        :param object_id: str, object id
        :return: shiftcontent.search_service
        """
        try:
            self.es.delete(
                index=self.index_name(index_name),
                doc_type=self.doc_type,
                id=object_id
            )
        except ex.NotFoundError:
            pass

        return self

    def search(self, body):
        """
        Search
        Execute search query
        :param body: dict, elasticsearch query
        :return: dict
        """
        results = self.es.search(
            index=self.index_name,
            body=body
        )

        return results








