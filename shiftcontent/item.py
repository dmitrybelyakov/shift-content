from shiftcontent import exceptions as x
import json
import copy
import arrow
from pprint import pprint as pp


class Item:
    """
    Content item
    This is a dto model for a content item. It holds a few generic meta fields
    and a set of configured custom fields. In addition provides representations
    for viewing, caching and searching.
    """
    # metadata fields
    metafields = {
        'id': 'integer',
        'created': 'datetime_meta',
        'type': 'text',
        'path': 'text',
        'sort_order': 'integer',
        'author': 'text',
        'object_id': 'text',
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
    }

    # impossible to change after creation
    frozen_metafields = (
        'id',
        'object_id',
        'author',
        'type',
        'created'
    )

    # content type definition and field types mapping
    _definition = None
    _field_types = None

    # meta fields + custom fields
    fields = None

    def __init__(self, *_, **kwargs):
        """
        Instantiate item
        Can optionally populate itself from keyword arguments
        :param type: str, content type of the item
        :param kwargs: dict, key-value pairs used to populate the item
        """

        # init meta fields
        self.fields = dict()
        for field, field_type in self.metafields.items():
            self.fields[field] = self.field_types[field_type]()

        # populate from kwargs
        if kwargs:
            self.from_dict(kwargs, initial=True)

        # set sort order
        if self.fields['sort_order'].get() is None:
            self.set_field('sort_order', 0)

        # set creation date
        if not self.fields['created'].get():
            self.set_field('created', arrow.utcnow().datetime, initial=True)

    @property
    def definition(self):
        """
        Definition
        Returns content type definition based on content type property or
        throws an exception if not found.
        :return: dict
        """
        if not self._definition:
            try:
                from shiftcontent import definition_service
                self._definition = definition_service.get_type(self.type)
            except x.UndefinedContentType:
                err = 'Unable to set content type: [{}] is undefined'
                raise x.ItemError(err.format(self.type))

        return self._definition

    @property
    def field_types(self):
        """
        Field types
        Returns a dictionary of field types.
        :return: dict
        """
        if not self._field_types:
            from shiftcontent.field_types import field_types
            self._field_types = field_types
        return self._field_types

    def __repr__(self):
        """ Returns printable representation of item """
        repr = '<ContentItem id=[{}] object_id=[{}]>'
        return repr.format(self.id, self.object_id)

    def __getattr__(self, item):
        """
        Get attribute
        Overrides attribute access for getting props and fields
        :param item: str, property name
        :return:
        """
        if item in self.fields:
            return self.fields[item].get()
        return object.__getattribute__(self, item)

    def __setattr__(self, key, value):
        """
        Set attribute
        Overrides attribute access for setting props and fields
        :param key: str, property name
        :param value: value to set
        :return: shiftcontent.item.Item
        """
        if self.fields and key in self.fields:
            self.set_field(key, value)
        else:
            object.__setattr__(self, key, value)

    def init_fields(self):
        """
        Initialize fields
        Retrieves content type definition schema ant initializes the
        fields.
        :return: shiftcontent.item.Item
        """
        for field in self.definition['fields']:
            handle = field['handle']
            field_type = field['type']
            if handle not in self.fields:
                self.fields[handle] = self.field_types[field_type]()
        return self

    def set_field(
        self,
        field,
        value,
        initial=False,
        from_db=False,
        from_json=False
    ):
        """
        Set field
        Inspects content type definition for field type and converts field
        value to this specific type (int, datetime, bool, etc).

        Will silently ignore fields that can't be set after initial
        initialization (frozen metafields), unless initial flag is set to True

        :param field: str, field name
        :param value: str, value to set
        :param initial: bool, is this initial instantiation?
        :param from_db: bool, use db setter on field
        :param from_json: bool, use json setter on field
        :return: shiftcontent.item.Item
        """
        # skip frozen unless initial set
        if field in self.frozen_metafields and not initial:
            return self

        # get setter name
        if from_db:
            setter_name = 'from_db'
        elif from_json:
            setter_name = 'from_json'
        else:
            setter_name = 'set'

        # set type first and init custom fields
        if field == 'type':
            field_type = self.field_types[self.metafields['type']]()
            self.fields['type'] = field_type
            getattr(self.fields['type'], setter_name)(value)
            self.init_fields()
            return

        if field not in self.fields.keys():
            return

        # set fields
        getattr(self.fields[field], setter_name)(value)
        return self

    def is_updatable(self, field):
        """
        Is updatable
        Checks if field exists and is allowed to be updated.
        :param field: str, field handle
        :return:
        """
        return field in self.fields and field not in self.frozen_metafields

    # --------------------------------------------------------------------------
    # Representations
    # --------------------------------------------------------------------------

    def to_dict(self):
        """
        To dict
        Returns dictionary representation of an item.
        :return: dict
        """
        data = {p: v.get() for p, v in self.fields.items()}
        return data

    def from_dict(self, data, initial=False):
        """
        From dict
        Populates itself from a dictionary. Will ignore fields that can't be
        updated after being initially set, unless initial is switched to True.

        :param data: dict, fields:values to set
        :param initial: bool, whether this is an initial field set
        :return: shiftcontent.item.Item
        """
        data = copy.copy(data)

        # first, set type to initialize custom fields
        if initial and 'type' in data:
            self.set_field('type', data['type'], initial)
            del data['type']

        # set the rest of the fields
        for field, value in data.items():
            self.set_field(field, value, initial=initial)
        return self

    def to_db(self, update=True):
        """
        To db
        Returns database representation of item ready to be persisted in
        content items table. Additionally will drop fields that are forbidden
        to be updated unless update flag is set to False
        :param update: bool, is it an update or initial insert?
        :return: dict
        """
        data = dict()
        fields = dict()
        for field, value in self.fields.items():
            if field not in self.metafields:
                fields[field] = value.to_db()
            else:
                data[field] = value.to_db()

        # jsonify custom fields
        data['fields'] = json.dumps(fields, ensure_ascii=False)

        # for updates, filter out unchangeable fields
        if update:
            for frozen in self.frozen_metafields:
                del data[frozen]

        # and return
        return data

    def from_db(self, data):
        """
        From db
        Populates itself back from data stored in database and decodes
        json fields
        :param data: dict, data from the database
        :return: shiftcontent.itemItem
        """
        fields = json.loads(data['fields'])
        data = {**data, **fields}
        del data['fields']

        # first, set type to initialize custom fields
        if 'type' in data:
            self.set_field('type', data['type'], initial=True)
            del data['type']

        # now set the rest of the fields
        for name, value in data.items():
            self.set_field(name, value, initial=True, from_db=True)

        return self

    def to_search(self):
        """
        To search
        Returns representation sutable for putting to search index
        :return: dict
        """
        data = {f: v.to_search() for f, v in self.fields.items()}
        return data

    def to_json(self, as_string=True):
        """
        To json
        Returns json representation of the item. This useful for putting
        to cache. Has an optional flag indicating whether a string should
        be returned or just a dict with all values stringified.
        :param as_string: bool, strinify or return as dict
        :return: str | dict
        """
        data = {f: v.to_json() for f, v in self.fields.items()}

        # return dict to jsonify later?
        if not as_string:
            return data

        jsonified = json.dumps(data, ensure_ascii=True)
        return jsonified

    def from_json(self, json_data):
        """
        From json
        Populates itself from a json string
        :param json_data: str, json string
        :return: shiftcontent.item.Item
        """
        try:
            data = json.loads(json_data, encoding='utf-8')
        except json.JSONDecodeError:
            raise x.ItemError('Failed to decode json')

        # first, set type to initialize custom fields
        if 'type' in data:
            self.set_field('type', data['type'], initial=True)
            del data['type']

        # now set the rest of the fields
        for name, value in data.items():
            self.set_field(name, value, initial=True, from_json=True)

        return self






