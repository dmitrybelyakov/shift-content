from shiftcontent import exceptions as x
import json
import copy
import arrow
from pprint import pprint as pp


class Item:
    """
    Content item
    Represents a projection of a content item
    """

    # datetime format
    date_format = '%Y-%m-%d %H:%M:%S'

    # metadata fields
    meta = None
    valid_metafields = (
        'id',
        'created',
        'type',
        'path',
        'author',
        'object_id',
        # 'version',
        # 'parent_version',
        # 'status',
        # 'lat',
        # 'long',
        # 'categories',
        # 'tags',
        # 'comments',
        # 'reactions',
        # 'upvotes',
        # 'downvotes',
    )

    # impossible to change after creation
    frozen_metafields = (
        'id',
        'object_id',
        'author',
        'type'
    )

    # content type fields
    valid_fields = None
    fields = None


    # TODO: RENDER REPRESENTATION AVAILABLE TO CLIENTS
    # TODO: HOW DO WE DECODE DATA PICKELED IN JSON FOR FIELD TYPES? (DATES)
    # TODO: WHAT ARE OTHER FIELD TYPES THAT WE HAVE



    def __init__(self, type, **kwargs):
        """
        Instantiate item
        Can optionally populate itself from kwargs
        :param type: str, content type of the item
        :param kwargs: dict, key-value pairs used to populate the item
        """
        try:
            from shiftcontent import definition_service
            type_definition = definition_service.get_type(type)
        except x.UndefinedContentType:
            err = 'Unable to create item. Content type [{}] is undefined'
            raise x.ItemError(err.format(type))

        # init meta
        meta = {prop: None for prop in self.valid_metafields}
        meta['type'] = type
        self._set('meta', meta)

        # init valid type fields
        valid_fields = [f['handle'] for f in type_definition['fields']]
        self._set('valid_fields', valid_fields)

        # init fields
        fields = {field: None for field in self.valid_fields}
        self._set('fields', fields)

        # populate from dict if got kwargs
        self.from_dict(kwargs)
        if not self.meta['created']:
            self.meta['created'] = arrow.utcnow().datetime

    def __repr__(self):
        """ Returns printable representation of item """
        repr = '<ContentItem id=[{}] object_id=[{}]>'
        return repr.format(self.id, self.object_id)

    def __getattr__(self, item):
        """ Overrides attribute access for getting props and fields """
        if item in self.meta:
            return self.meta[item]
        elif item in self.fields:
            return self.fields[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """ Overrides attribute access for setting props and fields """
        if key == 'fields':
            self.set_fields(value)
        elif key == 'meta':
            self.set_meta(value)
        elif key in self.valid_fields:
            self.fields[key] = value
        elif key in self.meta:
            if key == 'created' and type(value) is str:
                value = arrow.get(value).datetime
            self.meta[key] = value
        else:
            self._set(key, value)

        return self

    def _set(self, property, value):
        """
        Internal set
        Sets a property on itself avoiding overloading magic.
        :param prop: str, property to set
        :param val: vaue
        :return: shiftcontent.content.ContentService
        """
        object.__setattr__(self, property, value)
        return self

    def is_updatable(self, field):
        """
        Is updatable
        Checks if field exists and is allowed to be updated.

        :param field: str, field handle
        :return:
        """
        if field in self.valid_fields or field in self.valid_metafields:
            if field not in self.frozen_metafields:
                return True

        return False

    def set_meta(self, meta):
        """
        Set meta
        Accepts a dictionary of meta fields to set.
        :param meta:
        :return:
        """
        if type(meta) is not dict:
            msg = 'Meta fields must be a dictionary, got {}'
            raise x.ItemError(msg.format(type(meta)))

        for prop, val in meta.items():
            if prop in self.valid_metafields:
                if prop == 'created' and type(val) is str:
                    val = arrow.get(val).datetime
                self.meta[prop] = val

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
                raise x.ItemError('Failed to decode fields string')

        if type(fields) is not dict:
            msg = 'Fields must be a dictionary, got {}'
            raise x.ItemError(msg.format(type(fields)))

        for prop, val in fields.items():
            if prop in self.valid_fields:
                self.fields[prop] = val

    # --------------------------------------------------------------------------
    # Representations
    # --------------------------------------------------------------------------

    def to_db(self, update=True):
        """
        To db
        Returns database representation for persistence. Same as to_dict but
        fields are stringified. Additionally will drop fields that are
        forbidden to change on existing items
        :return:
        """
        data = copy.copy(self.meta)
        data['fields'] = json.dumps(self.fields, ensure_ascii=False)

        # for updates, filter out unchangeable fields
        if update:
            del data['type']
            del data['id']
            del data['object_id']
            del data['author']

        return data

    def to_dict(self, serialized=False):
        """
        Returns dictionary representation of the item. Can optionally
        serialize fields, e.g. datetimes to strings
        :param serialized:
        :return: dict
        """
        data = copy.copy(self.fields)
        data['meta'] = copy.copy(self.meta)

        # serialize?
        if serialized:
            data['meta']['created'] = data['meta']['created'].strftime(
                self.date_format
            )

        return data

    def from_dict(self, data):
        """
        From dict
        Populates itself from a dictionary
        :param data: dict, data to populate from
        :return: shiftcontent.item.Item
        """
        for p, v in data.items():
            if p in ['meta', 'fields'] or p in self.meta or p in self.fields:
                setattr(self, p, v)
        return self

    def to_search(self):
        """
        To search
        Returns representation suitable for putting into the search index.
        :return: dict
        """

        # todo: implement this
        return self.to_dict(serialized=True)

    def serialize(self):
        """
        Serialize
        Returns serialized representation of item suitable for storage in
        event store or cache
        :return: dict
        """
        raise NotImplemented

    def unserialize(self, data):
        """
        Unserialize
        Accepts serialized data and populates itself from it.
        :param data: dict
        :return: shiftcontent.item.Item
        """
        raise NotImplemented





