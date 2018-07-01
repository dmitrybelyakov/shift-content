from shiftcontent import exceptions as x
import json
import copy
from datetime import datetime


class Item:
    """
    Content item
    Represents a projection of a content item
    """
    # item props, initialized at instance level
    props = dict()

    def __init__(self, *_, **kwargs):
        """
        Instantiate item
        Can optionally populate itself from kwargs
        :param _: args, ignored
        :param kwargs: dict, key-value pairs used to populate the item
        """
        # init props
        self.props = dict(
            id=None,
            created=None,
            type=None,
            path=None,
            author=None,
            object_id=None,
            data=None
        )
        self.from_dict(kwargs)
        if not self.props['created']:
            self.props['created'] = datetime.utcnow()

        # todo: version
        # todo: parent_version
        # todo: status

        # todo: lat
        # todo: long
        # todo: categories
        # todo: tags
        # todo: comments
        # todo: reactions [like]
        # todo: uvotes
        # todo: downvotes

    def __repr__(self):
        """ Returns printable representation of item """
        repr = '<ContentItem id=[{}] object_id=[{}]>'
        return repr.format(self.id, self.object_id)

    def __getattr__(self, item):
        """ Overrides attribute access for getting props """
        if item in self.props:
            return self.props[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """ Overrides attribute access for setting props"""
        if key == 'data':
            self.set_data(value)
        elif key in self.props:
            self.props[key] = value
            return self
        else:
            object.__setattr__(self, key, value)
        return self

    def set_data(self, data):
        """
        Set data
        Accepts a dictionary and encodes it into a json string for persistence.
        Will raise an exception if data is not a dictionary.
        :param payload: dict
        :return:
        """
        if type(data) is str:
            try:
                data = json.loads(data, encoding='utf-8')
            except json.JSONDecodeError:
                raise x.ContentItemError('Failed to decode data string')

        if type(data) is not dict:
            msg = 'Data must be a dictionary, got {}'
            raise x.ContentItemError(msg.format(type(data)))
        self.props['data'] = data
        return self

    def to_dict(self):
        """ Returns dictionary representation of the item """
        return copy.copy(self.props)

    def to_db(self):
        """
        To db
        Returns database representation for persistence. Same as to_dict but
        data is stringified.
        :return:
        """
        data = self.to_dict()
        data['data'] = json.dumps(data['data'], ensure_ascii=False)
        return data

    def from_dict(self, data):
        """ Populates itself from a dictionary """
        for prop, val in data.items():
            if prop in self.props:
                setattr(self, prop, val)
        return self

