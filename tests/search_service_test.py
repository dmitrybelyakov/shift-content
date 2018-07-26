from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from pprint import pprint as pp
from shiftcontent.search_service import SearchService


@attr('search', 'service')
class SearchServiceTest(BaseTestCase):

    def test_create_search_service(self):
        """ Creating search service"""
        service = SearchService()
        self.assertIsInstance(service, SearchService)
