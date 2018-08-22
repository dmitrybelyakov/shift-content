from shiftcontent import exceptions as x
import json
import copy
import arrow
from datetime import datetime
from pprint import pprint as pp

# TODO: do we define mapping separately (view, search)
# TODO: or do we encapsulate it in field type?

# TODO: whichever we choose we'll need sme processor to handle type conversions
# TODO: for each type so we can serialize-deserialize data from-to db/cache

# TODO: how do we store/process mapping for meta fields (view and search)?
# TODO: this should probably treated as a special case, e.g. meta geopoint

"""

VIEW MAPPING (python data types)

  * text
  * int
  * float
  * bool
  * date
  * datetime
  
DATABASE MAPPING (special mapping if not auto serializable to json)
  * date
  * datetime   
  
SEARCH MAPPING (elasticsearch data types)
  * text
  * keyword
  * boolean
  * integer
  * long
  * float
  * double
  

"""


class Item:
    """
    Content item
    This is a dto model for a content item. It holds a few generic metafields
    and a set of configured custom fields. In addition provides representations
    for viewing, caching and searching.
    """

    # datetime format
    date_format = '%Y-%m-%d %H:%M:%S'

    # metadata fields
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

        # init metafields
        self.fields = {prop: None for prop in self.valid_metafields}

        # populate from kwargs
        if kwargs:
            self.from_dict(kwargs, initial=True)

        # set creation date
        if not self.fields['created']:
            self.fields['created'] = arrow.utcnow().datetime

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
            return self.fields[item]
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
            if handle not in self.fields:
                self.fields[handle] = None
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
            self.fields['type'] = value
            self.init_fields()

        if field not in self.fields.keys():
            return

        # set metafields
        if field in self.valid_metafields:
            if field == 'created' and type(value) is str:
                self.fields['created'] = arrow.get(value).datetime
                return

        # todo: do type conversion here

        # set custom fields
        self.fields[field] = value
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

    def to_dict(self, serialized=False):
        """
        To dict
        Returns dictionary representation of an item. Can optionally serialize
        values to strings
        :param serialized: bool, whether to serialize values
        :return: dict
        """
        data = copy.copy(self.fields)
        if serialized:
            for field, value in data.items():
                if type(value) is datetime:
                    data[field] = value.strftime(self.date_format)

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
                fields[field] = value
            else:
                data[field] = value

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
        for field, value in fields.items():
            data[field] = value

        self.from_dict(data, initial=True)
        return self

    def to_search(self):
        """
        To search
        Returns representation sutable for putting to search index
        :return: dict
        """
        data = copy.copy(self.fields)
        full_text = ('{}: {}\n'.format(f, v) for f, v in data.items())
        data['full_text'] = ''.join(full_text)
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
        serialized = self.to_dict(serialized=True)

        # return dict to jsonify later?
        if not as_string:
            return serialized

        jsonified = json.dumps(serialized, ensure_ascii=True)
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






