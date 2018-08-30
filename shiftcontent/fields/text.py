from .abstract import AbstractFieldType


class Text(AbstractFieldType):

    def set(self, value):
        """
        Sets field value
        :param value: str, field value
        :return: shiftcontent.fields.text.Text
        """
        if value is None:
            return self

        self.value = str(value)
        return self

    def get(self):
        """
        Returns current field value
        :return: str
        """
        return self.value

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
        :return: shiftcontent.fields.text.Text
        """
        self.set(value)
        return self

    def to_json(self):
        """
        Returns json representation of value
        :return: str
        """
        return self.value

    def from_json(self, value):
        """
        Populate field value from json representation
        :param value: str or date
        :return: shiftcontent.fields.text.Text
        """
        self.set(value)
        return self

    def to_search(self):
        """
        Returns search representation of value
        :return: str
        """
        return self.value

    def search_mapping(self):
        """
        Returns search index data type for the value
        :return: str
        """
        return 'text'

