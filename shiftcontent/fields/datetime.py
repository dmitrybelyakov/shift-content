from .abstract import AbstractFieldType
import arrow
from datetime import datetime


class DateTime(AbstractFieldType):

    def set(self, value):
        """
        Sets field value.
        Accepts a datetime string in a specific format and converts it to a
        datetime object. Will assume the date is in UTC timezone.

        :param value: mixed, field value
        :return: shiftcontent.fields.text.DateTime
        """
        format = 'YYYY-MM-DD HH:mm:ss'
        if value is not None:
            if type(value) is not datetime:
                arr = arrow.get(str(value), format).to('UTC')
                value = arr.datetime

        self.value = value
        return self

    def get(self):
        """
        Returns current field value
        :return: datetime
        """
        return self.value

    def to_db(self):
        """
        Returns db representation of value
        :return: str
        """
        return self.value.strftime('%Y-%m-%d %H:%M:%S')

    def from_db(self, value):
        """
        Populate field value from db representation
        :param value: str or date
        :return: shiftcontent.fields.text.DateTime
        """
        self.set(value)
        return self

    def to_json(self):
        """
        Returns json representation of value
        :return: str
        """
        return self.value.strftime('%Y-%m-%d %H:%M:%S')

    def from_json(self, value):
        """
        Populate field value from json representation
        :param value: str or date
        :return: shiftcontent.fields.text.DateTime
        """
        self.set(value)
        return self

    def to_search(self):
        """
        Returns search representation of value
        :return: datetime
        """
        return self.value

    def search_mapping(self):
        """
        Returns search index data type for the value
        :return: str
        """
        return dict(
            type='date'
        )

