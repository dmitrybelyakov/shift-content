from .abstract import AbstractFieldType


class Boolean(AbstractFieldType):

    def set(self, value):
        """
        Sets field value
        :param value: mixed, field value
        :return: shiftcontent.fields.text.Boolean
        """
        if value is None:
            return self

        if value in ('False', '0', 'no'):
            value = False

        if value in ('True', '1', 'yes'):
            value = True

        self.value = bool(value)
        return self

    def get(self):
        """
        Returns current field value
        :return: bool
        """
        return self.value

    def to_db(self):
        """
        Returns db representation of value
        :return: bool
        """
        return self.value

    def from_db(self, value):
        """
        Populate field value from db representation
        :param value: str or bool
        :return: shiftcontent.fields.text.Boolean
        """
        self.set(value)
        return self

    def to_json(self):
        """
        Returns json representation of value
        :return: bool
        """
        return self.value

    def from_json(self, value):
        """
        Populate itself from json representation of value
        :param value: bool
        :return: shiftcontent.fields.text.Boolean
        """
        self.set(value)
        return self

    def to_search(self):
        """
        Returns search representation of value
        :return: bool
        """
        return self.value

    def search_mapping(self):
        """
        Returns search index data type for the value
        :return: str
        """
        return 'boolean'

