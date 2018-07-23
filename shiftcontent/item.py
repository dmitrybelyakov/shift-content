from shiftcontent import exceptions as x
import json
import copy
from datetime import datetime
from shiftcontent.services import definition



# TODO: REFACTOR ME I WANNA BE PRETTY


class Item:
    """
    Content item
    Represents a projection of a content item
    """



    # item props, initialized at instance level
    props = dict()

    def __init__(self, type, **kwargs):
        """
        Instantiate item
        Can optionally populate itself from kwargs
        :param type: str, content type of the item
        :param kwargs: dict, key-value pairs used to populate the item
        """
        try:
            type_definition = definition.get_type_schema(type)
        except x.UndefinedContentType:
            err = 'Unable to create item. Content type [{}] is undefined'
            raise x.ContentItemError(err.format(type))

        item_fields = (field['handle'] for field in type_definition['fields'])
        self.props = dict(
            id=None,
            created=None,
            type=type,
            path=None,
            author=None,
            object_id=None,
            fields={field: None for field in item_fields}
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
        """ Overrides attribute access for getting props and fields  """
        if item == 'props':
            return self.props
        if self.props['fields'] and item in self.props['fields']:
            return self.props['fields'][item]
        if item in self.props:
            return self.props[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """ Overrides attribute access for setting props and fields """
        if key == 'fields':
            self.set_fields(value)
        elif 'fields' in self.props and key in self.props['fields']:
            self.props['fields'][key] = value
        elif key in self.props:
            self.props[key] = value
            return self
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

        fields = {k: v for k, v in fields.items() if k in self.props['fields']}
        self.props['fields'] = fields
        return self

    def to_dict(self):
        """ Returns dictionary representation of the item """
        return copy.copy(self.props)

    def to_db(self):
        """
        To db
        Returns database representation for persistence. Same as to_dict but
        fields are stringified.
        :return:
        """
        data = self.to_dict()
        data['fields'] = json.dumps(data['fields'], ensure_ascii=False)
        return data

    def from_dict(self, data):
        """ Populates itself from a dictionary """
        for prop, val in data.items():
            if prop in self.props or prop in self.props['fields']:
                setattr(self, prop, val)
        return self

