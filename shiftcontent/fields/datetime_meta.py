from .datetime import DateTime
import arrow
from datetime import datetime


class DateTimeMeta(DateTime):

    def to_db(self):
        """
        Returns db representation of value
        :return: str
        """
        return self.value

    def from_db(self, value):
        """
        Populate field value from db representation
        :param value: str or date
        :return: shiftcontent.fields.text.DateTimeMetaField
        """
        self.set(value)
        return self

    def from_json(self, value):
        """
        Populate field value from json representation
        :param value: str or date
        :return: shiftcontent.fields.text.DateTimeMetaField
        """
        self.set(value)
        return self

