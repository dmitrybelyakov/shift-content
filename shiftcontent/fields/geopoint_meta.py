from .abstract import AbstractFieldType


class GeopointMeta(AbstractFieldType):

    def set(self, value):
        """
        Sets field value
        :param value: dict, latitude and longitude
        :return: shiftcontent.fields.text.GeopointMeta
        """
        if value is not None:
            if type(value) is not dict:
                raise ValueError('Geopoint must be a dict')
            if 'lat' not in value or 'lon' not in value:
                raise ValueError('Geopoint must contain [lat] and [lon]')

            value = {**value}
            value['lat'] = float(value['lat'])
            value['lon'] = float(value['lon'])

        self.value = value
        return self

    def get(self):
        """
        Returns current field value
        :return: dict[float, float]
        """
        return self.value

    def to_db(self):
        """
        Returns db representation of value
        :return: int
        """
        return '{},{}'.format(self.value['lat'], self.value['lon'])

    def from_db(self, value):
        """
        Populate field value from db representation
        :param value: str
        :return: shiftcontent.fields.text.GeopointMeta
        """
        value = str(value).split(',')
        self.value = dict(
            lat=float(value[0]),
            lon=float(value[1]),
        )

        return self

    def to_json(self):
        """
        Returns json representation of value
        :return: dict[float, float]
        """
        return self.value

    def from_json(self, value):
        """
        Populate itself from json representation of value
        :param value: dict[float, float]
        :return: shiftcontent.fields.text.GeopointMeta
        """
        self.set(value)
        return self

    def to_search(self):
        """
        Returns search representation of value
        :return: int
        """
        return self.value

    def search_mapping(self):
        """
        Returns search index data type for the value
        :return: str
        """
        return 'geo_point'

