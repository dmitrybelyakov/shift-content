from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import exceptions as ex
from pprint import pprint as pp

from shiftcontent import definition_service


class SearchService:

    def __init__(self, *_, **kwargs):
        """
        Init service
        If any kwargs are given to constructor, a delayed initializer is
        called with these kwargs. This class only accepts kwargs.
        """

        # es connection [host:port]
        self.hosts = []

        # es instance
        self._es = None

        # index name
        self.index_name = None
        # document type
        self.doc_type = None

        if kwargs:
            self.init(**kwargs)

    def init(
        self,
        *,
        hosts=('localhost:9002',),
        index_name=None,
        doc_type='content'):
        """
        Delayed service initializer. Called either by constructor if args
        passed in, or later in userland code to configure the service.

        :param hosts: iterable, hosts (and ports) to connect to
        :param port: int, elasticsearch port
        :param index_name: str, index name
        :param doc_type: str, document type
        :return: shiftcontent.search_service.SearchService
        """
        self.hosts = hosts
        self.index_name = index_name
        self.doc_type = doc_type

        return self

    @property
    def es(self):
        """
        Elasticsearch instance
        :return:
        """
        if not self._es:
            self._es = Elasticsearch(self.hosts)
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




