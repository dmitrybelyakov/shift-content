from abc import ABCMeta, abstractmethod


class AbstractFieldType(metaclass=ABCMeta):
    """
    Abstract field type
    Defines the interface your concrete field types must implement.
    A field type is used to do data conversions from the data stored to various
    representation, like json, search etc. This is how you can tell certain
    fields to be of specific data types whn put to index or cache, or loaded
    back into your application.
    """

    def __init__(self, value=None):
        self.value = None
        if value is not None:
            self.set(value)

    @abstractmethod
    def set(self, value):  # pragma: no cover
        """
        Set data, can accept proper data type or a string
        :param value: mixed
        :return: self
        """
        pass

    @abstractmethod
    def get(self):   # pragma: no cover
        """
        Get view representation of value. This will depend on your concrete
        field type implementation
        :return: mixd
        """
        pass

    @abstractmethod
    def to_db(self):  # pragma: no cover
        """
        Get db representation of field. This data type should be json
        serializable.
        :return: mixed
        """
        pass

    @abstractmethod
    def from_db(self, value):  # pragma: no cover
        """
        Populate field value from its db representation
        :param value: mixed
        :return: self
        """
        pass

    @abstractmethod
    def to_json(self):  # pragma: no cover
        """
        Return JSON serializable version of value
        :return:
        """
        pass

    def from_json(self, value):  # pragma: no cover
        """
        Populate field value from its json representation
        :param value: mixed
        :return: self
        """
        pass

    @abstractmethod
    def to_search(self):  # pragma: no cover
        """
        Return search representation of field. This will depend on your search
        mapping and can sometimes event result in having several nested fields
        for example for geopoint or range fields.
        :return: mixed
        """
        pass

    @abstractmethod
    def search_mapping(self):  # pragma: no cover
        """
        Type of field in elasticsearch index.
        For possible values see docs: http://bit.ly/2wnpazF
        :return: string
        """
        pass



