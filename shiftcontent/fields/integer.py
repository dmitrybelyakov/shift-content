from .abstract import AbstractFieldType


class Integer(AbstractFieldType):

    def set(self, value):
        """
        Sets field value
        :param value: mixed, field value
        :return: shiftcontent.fields.text.Integer
        """
        if value is None:
            return self

        self.value = int(float(value))
        return self

    def get(self):
        """
        Returns current field value
        :return: int
        """
        return self.value

    def to_db(self):
        """
        Returns db representation of value
        :return: int
        """
        return self.value

    def from_db(self, value):
        """
        Populate field value from db representation
        :param value: str or date
        :return: shiftcontent.fields.text.Integer
        """
        self.set(value)
        return self

    def to_json(self):
        """
        Returns json representation of value
        :return: int
        """
        return self.value

    def from_json(self, value):
        """
        Populate field value from json representation
        :param value: str or date
        :return: shiftcontent.fields.text.Integer
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
        return 'long'

