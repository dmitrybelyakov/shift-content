from datetime import datetime
from shiftcontent import exceptions as x
import json

class Event:
    """
    Event
    Represent single atomic operation.
    """
    # event props, initialized at instance level
    props = dict()

    def __init__(self, *_, **kwargs):
        """
        Instantiate event object
        Can optionally populate itself from kwargs
        :param _: args, ignored
        :param kwargs: dict, key-value pairs used to populate event
        """
        # init props
        self.props = dict(
            id=None,
            created=None,
            type=None,
            author=None,
            object_id=None,
            payload=None
        )

        self.from_dict(kwargs)
        if not self.props['created']:
            self.props['created'] = datetime.utcnow()

    def __repr__(self):
        """ Returns printable representation of an event """
        repr = '<ContentEvent id=[{}] object_id=[{}] type=[{}] created={}>'
        return repr.format(self.id, self.object_id, self.type, self.created)

    def __getattr__(self, item):
        """ Overrides attribute access for getting props """
        if item == 'payload':
            return self.get_payload()
        if item in self.props:
            return self.props[item]
        return getattr(self, item)

    def __setattr__(self, key, value):
        """ Overrides "attribute access for setting props"""
        if key == 'id':
            raise x.EventError('Modifying event id is forbidden')
        if key == 'payload':
            self.set_payload(value)
        elif key in self.props:
            self.props[key] = value
            return self
        else:
            object.__setattr__(self, key, value)
        return self

    def get_payload(self):
        """
        Get payload
        Decodes payload string into a dictionary and returns.
        :return: dict
        """
        payload = self.props['payload']
        if payload:
            payload = json.loads(payload, encoding='utf-8')
        return payload

    def set_payload(self, payload):
        """
        Set payload
        Accepts a dictionary and encodes it into a json string for persistence.
        Will raise an exception if payload is not a dictionary.
        :param payload: dict
        :return:
        """
        if type(payload) is not dict:
            raise x.EventError('Payload must be a dictionary')
        self.props['payload'] = json.dumps(payload, ensure_ascii=False)
        return self

    def to_dict(self):
        """ Returns dictionary representation of the event """
        return self.props

    def from_dict(self, data):
        """ Populates itself from a dictionary """
        for prop, val in data.items():
            if prop in self.props:
                setattr(self, prop, val)
        return self










