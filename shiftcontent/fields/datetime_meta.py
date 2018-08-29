from .datetime import DateTime
import arrow
from datetime import datetime


class DateTimeMetaField(DateTime):

    def to_db(self):
        """
        Returns db representation of value
        :return: str
        """
        return self.value

