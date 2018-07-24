from shiftcontent import exceptions as x
import json
import copy
from datetime import datetime
from pprint import pprint as pp

class Item:
    """
    Content item
    Represents a projection of a content item
    """

    # metadata fields
    meta = dict()

    # valid custom fields
    valid_fields = []

    # custom fields
    fields = dict()

    def __init__(self, type, **kwargs):
        """
        Instantiate item
        Can optionally populate itself from kwargs
        :param type: str, content type of the item
        :param kwargs: dict, key-value pairs used to populate the item
        """
        try:
            from shiftcontent import definition
            type_definition = definition.get_type_schema(type)
        except x.UndefinedContentType:
            err = 'Unable to create item. Content type [{}] is undefined'
            raise x.ContentItemError(err.format(type))

        # init fields
        self.valid_fields = [f['handle'] for f in type_definition['fields']]
        self.fields = {field: None for field in self.valid_fields}

        # init meta
        self.meta = dict(
            id=None,
            created=None,
            type=type,
            path=None,
            author=None,
            object_id=None,
            # version=None,
            # parent_version=None,
            # status=None,
            # lat=None,
            # long=None,
            # categories=None,
            # tags=None,
            # comments=None,
            # reactions=None,
            # upvotes=None,
            # downvotes=None,
        )


        # populate from dict if got kwargs
        self.from_dict(kwargs)
        if not self.meta['created']:
            self.meta['created'] = datetime.utcnow()

    def __repr__(self):
        """ Returns printable representation of item """
        repr = '<ContentItem id=[{}] object_id=[{}]>'
        return repr.format(self.id, self.object_id)

    def __getattr__(self, item):
        """ Overrides attribute access for getting props and fields  """
        if item in self.meta:
            return self.meta[item]
        elif item in self.fields:
            return self.fields[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """ Overrides attribute access for setting props and fields """
        if key == 'fields':
            self.set_fields(value)
        elif key in self.valid_fields:
            self.fields[key] = value
        elif key in self.meta:
            self.meta[key] = value
        else:
            object.__setattr__(self, key, value)

        return self

    def set_fields(self, fields):
        """
        Set fields
        Accepts a dictionary and encodes it into a json string for persistence.
        Will raise an exception if fields is not a dictionary.
        :param fields: dict
        :return:
        """
        if type(fields) is str:
            try:
                fields = json.loads(fields, encoding='utf-8')
            except json.JSONDecodeError:
                raise x.ContentItemError('Failed to decode fields string')

        if type(fields) is not dict:
            msg = 'Fields must be a dictionary, got {}'
            raise x.ContentItemError(msg.format(type(fields)))

        for prop, val in fields.items():
            if prop in self.valid_fields:
                self.fields[prop] = val

    def to_dict(self):
        """ Returns dictionary representation of the item """
        return {**self.meta, **self.fields}

    def to_db(self):
        """
        To db
        Returns database representation for persistence. Same as to_dict but
        fields are stringified.
        :return:
        """
        data = copy.copy(self.meta)
        data['fields'] = json.dumps(self.fields, ensure_ascii=False)
        return data

    def from_dict(self, data):
        """ Populates itself from a dictionary """
        for prop, val in data.items():
            if prop == 'fields' or prop in self.meta or prop in self.fields:
                setattr(self, prop, val)

        return self

