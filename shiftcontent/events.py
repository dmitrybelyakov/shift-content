from datetime import datetime


class Event:
    """
    Event
    Represent single atomic operation.
    """
    props = dict(
        id=None,
        created=None,
        type=None,
        author=None,
        object_id=None,
        payload=None
    )

    def __init__(self, *_, **kwargs):
        """
        Instantiate event object
        Can optionally populate itself from kwargs
        :param _: args, ignored
        :param kwargs: dict, key-value pairs used to populate event
        """
        self.from_dict(kwargs)
        if not self.props['created']:
            self.props['created'] = datetime.utcnow()

    def __repr__(self):
        """ Returns printable representation of an event """
        repr = '<ContentEvent id=[{}] object_id=[{}] type=[{}] created={}>'
        return repr.format(self.id, self.object_id, self.type, self.created)

    def __getattr__(self, item):
        """ Overrides attribute access for getting props """
        if item in self.props:
            return self.props[item]
        return getattr(self, item)

    def __setattr__(self, key, value):
        """ Overrides "attribute access for setting props"""
        if key in self.props:
            self.props[key] = value
            return self
        object.__setattr__(self, key, value)
        return self

    def to_dict(self):
        """ Returns dictionary representation of the event """
        return self.props

    def from_dict(self, data):
        """ Populates itself from a dictionary """
        for prop, val in data.items():
            if prop in self.props:
                self.props[prop] = val
        return self





