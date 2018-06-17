from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.item import Item
from shiftcontent import exceptions as x
from datetime import datetime


@attr('item')
class EventTest(BaseTestCase):

    def test_instantiating_event(self):
        """ Instantiating item """
        item = Item()
        self.assertIsInstance(item, Item)

    def test_printable_repr(self):
        """ Getting printable representation of an item """
        item = Item()
        repr = item.__repr__()
        self.assertIn('<ContentItem', repr)

    def test_event_gets_creation_date_upon_instantiation(self):
        """ Event gets creation date upon instantiating """
        item = Item()
        self.assertIsInstance(item.props['created'], datetime)

    def test_property_access(self):
        """ Can use property access for getting item props"""
        item = Item()
        self.assertIsInstance(item.created, datetime)

    def test_property_access_set(self):
        """ Property access for setting item props"""
        dt = 'datetime!'
        item = Item()
        item.created = dt
        self.assertEquals(dt, item.props['created'])


