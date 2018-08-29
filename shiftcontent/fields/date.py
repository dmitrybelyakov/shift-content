from .abstract import AbstractFieldType
from datetime import date, datetime
import arrow


class Date(AbstractFieldType):

    def set(self, value):
        """
        Sets field value.
        Accepts a datetime string in a specific format and converts it to a
        datetime object. Will assume the date is in UTC timezone.

        :param value: mixed, field value
        :return: shiftcontent.fields.text.Date
        """
        if value is None:
            return self

        format = 'YYYY-MM-DD'

        if type(value) is not datetime:
            arr = arrow.get(str(value), format).to('UTC')
            value = arr.date()
        self.value = value
        return self

    def get(self):
        """
        Returns current field value
        :return: date
        """
        return self.value

    def to_db(self):
        """
        Returns db representation of value
        :return: str
        """
        return self.value.strftime('%Y-%m-%d')

    def to_json(self):
        """
        Returns json representation of value
        :return: str
        """
        return self.value.strftime('%Y-%m-%d')

    def to_search(self):
        """
        Returns search representation of value
        :return: date
        """
        return self.value

    def search_mapping(self):
        """
        Returns search index data type for the value
        :return: str
        """
        return 'date'


