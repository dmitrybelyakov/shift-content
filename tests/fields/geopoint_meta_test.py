from tests.base import BaseTestCase
from nose.plugins.attrib import attr

from shiftcontent.fields import GeopointMeta
import json


@attr('fields', 'field_geopoint_meta')
class FloatMeta(BaseTestCase):

    def test_instantiate_field(self):
        """ Instantiating geopoint meta field """
        field = GeopointMeta()
        field.set(None)
        self.assertIsInstance(field, GeopointMeta)

    def test_get_value(self):
        """ Getting value from geopoint meta field """
        value = dict(lat='36.733226', lon='138.462091')
        field = GeopointMeta(value)
        self.assertEquals(36.733226, field.get()['lat'])
        self.assertEquals(138.462091, field.get()['lon'])
        self.assertTrue(type(field.get()) is dict)

    def test_raise_when_setting_non_dict_geopoint(self):
        """ Geopoint meta field raises on setting non-dict geopoint """
        with self.assertRaises(ValueError) as cm:
             GeopointMeta('crap')
        self.assertIn('Geopoint must be a dict', str(cm.exception))

    def test_raise_when_missing_lat_or_lon(self):
        """ Geopoint meta field raises on missing lat or lon """
        with self.assertRaises(ValueError) as cm:
             GeopointMeta(dict())
        self.assertIn(
            'Geopoint must contain [lat] and [lon]',
            str(cm.exception)
        )

    def test_get_db_representation(self):
        """ Getting db representation of geopoint meta field value """
        value = dict(lat=36.733226, lon=138.462091)
        field = GeopointMeta(value)
        expected = '{},{}'.format(value['lat'], value['lon'])
        self.assertEquals(expected, field.to_db())
        self.assertTrue(type(field.to_db()) is str)

    def test_populate_from_db_representation(self):
        """ Populating value from db representation for geopoint meta field"""
        value = dict(lat=36.733226, lon=138.462091)
        db_value = '{},{}'.format(value['lat'], value['lon'])
        field = GeopointMeta()
        field.from_db(db_value)
        self.assertEquals(value, field.get())

    def test_get_json_representation(self):
        """ Getting json representation of geopoint meta field value """
        value = dict(lat=36.733226, lon=138.462091)
        field = GeopointMeta(value)
        self.assertEquals(value, field.to_json())

    def test_populate_from_json_representation(self):
        """ Populating value from json representation for geopoint meta field"""
        value = dict(lat=36.733226, lon=138.462091)
        field = GeopointMeta()
        field.from_json(value)
        self.assertEquals(value, field.get())

    def test_get_search_representation(self):
        """ Getting search representation of geopoint meta field value """
        value = dict(lat=36.733226, lon=138.462091)
        field = GeopointMeta(value)
        self.assertEquals(value, field.to_search())

    def test_get_search_mapping(self):
        """ Getting search index data type for the geopoint meta field """
        field = GeopointMeta()
        self.assertEquals('geo_point', field.search_mapping())





