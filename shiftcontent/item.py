from shiftcontent import exceptions as x
from shiftcontent import fields
import json
import copy
import arrow
from datetime import datetime
from pprint import pprint as pp

field_types = dict(
    text=fields.Text,
    boolean=fields.Boolean,
    date=fields.Date,
    datetime=fields.DateTime,
    datetime_meta=fields.DateTimeMetaField,
    integer=fields.Integer,
    float=fields.Float,
)


class Item:
    """
    Content item
    This is a dto model for a content item. It holds a few generic meta fields
    and a set of configured custom fields. In addition provides representations
    for viewing, caching and searching.
    """
    # metadata fields
    valid_metafields = {
        'id': 'integer',
        'created': 'datetime_meta',
        'type': 'text',
        'path': 'text',
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
        # self.fields = {prop: None for prop in self.valid_metafields.keys()}
        self.fields = dict()
        for field, field_type in self.valid_metafields.items():
            self.fields[field] = field_types[field_type]()

        # populate from kwargs
        if kwargs:
            self.from_dict(kwargs, initial=True)

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
        try:
            from shiftcontent import definition_service
            type_definition = definition_service.get_type(self.type)
            return type_definition
        except x.UndefinedContentType:
            err = 'Unable to set content type: [{}] is undefined'
            raise x.ItemError(err.format(self.type))

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
                self.fields[handle] = field_types[field_type]()
        return self

    def set_field(self, field, value, initial=False):
        """
        Set field
        Inspects content type definition for field type and converts field
        value to this specific type (int, datetime, bool, etc).

        Will silently ignore fields that can't be set after initial
        initialization (frozen metafields), unless initial flag is set to True

        :param field: str, field name
        :param value: str, value to set
        :param initial: bool, is this initial instantiation?
        :return: shiftcontent.item.Item
        """

        # skip frozen unless initial set
        if field in self.frozen_metafields and not initial:
            return self

        # init custom fields on first set
        if field == 'type':
            field_type = self.valid_metafields['type']
            self.fields['type'] = field_types[field_type](value)
            self.init_fields()

        if field not in self.fields.keys():
            return

        # set metafields
        if field == 'created' and type(value) is str:
            self.fields['created'].set(arrow.get(value).datetime)
            return

        # set custom fields
        self.fields[field].set(value)
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

        # set type fom dict (initializes custom fields)
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
        to be updated unles update flag is set to False
        :param update: bool, is it an update or initial insert?
        :return: dict
        """
        data = dict()
        fields = dict()
        for field, value in self.fields.items():
            if field not in self.valid_metafields:
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
        data = {**data}
        fields = json.loads(data['fields'])
        del data['fields']
        self.from_dict({**data, **fields}, initial=True)
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

        self.from_dict(data, initial=True)
        return self






