

# @todo: Implement media uploads outside event sourcing system
# @todo: Only store references to files in event sourcing system


class Module:
    id = None
    version = 'uuid'
    fields = []


class Version:
    """
    Represents a change set - a collection of events.
    We can rollback to this specific version by looking at all the events
    an getting their state
    """
    id = None
    parent_version = None
    created = None
    author = 'Identity'
    object = 'Module'
    object_id = 123
    events = []




class BaseEvent:
    """
    Will events be different per field?
    Is image event the same as text event?
    How do we track module updates?
    Module update is just a change to one of its fields.
    """
    id = None
    created = None
    author = 'Identity'
    object_type = 'field'
    object_id = 123
    payload = 'new_value'

    def update_state(self):
        """
        Apply state changes based on payload.
        This is can be a separate event handler, but it's nicer to have
        event processing logic and payload in one place.
        :return:
        """
        pass
