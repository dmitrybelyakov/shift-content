from shiftcontent.event import Event, EventSchema
from shiftcontent import exceptions as x


class EventService():
    """
    Event service
    Responsible for handling events
    """

    def __init__(self, db):
        """
        Initialize event service
        Accepts a database instance to operate on events and projections.
        :param db:
        """
        self.db = db

    def event(self, type, object_id, author, payload, emit=True):
        """
        Persist an event
        Creates a new event object, validates it and saves to the database.
        May throw a validation exception if some event data is invalid.

        :param type: str, event type
        :param object_id: str, an id of the object being affected
        :param author:  str, author id in external system
        :param payload: dict, event payload
        :param emit: bool, whether to call handler immediately
        :return: shiftcontent.event.Event
        """
        # create
        event = Event(
            type=type,
            author=author,
            object_id=object_id,
            payload=payload
        )

        # validate
        schema = EventSchema()
        ok = schema.process(event)
        if not ok:
            raise x.InvalidEvent(validation_errors=ok.get_messages())

        # and save
        self.db.append_event(event)

        # also emit?
        if emit:
            self.emit(event)

        return event

    def emit(self, event):
        """
        Emit event
        Triggers the corresponding error handler for an event and passes in
        the payload. This is used when creating new events or replaying events
        that were already saved.
        :param event: shiftcontent.event.Event
        :return:
        """
        if not event.id:
            raise x.EventError('To emit an event it must be saved first')

        # define events
        handlers = dict(
            CONTENT_ITEM_CREATE=self.content_item_create
        )

        # get handler
        handler = handlers[event.type] if event.type in handlers else None
        if not handler:
            raise x.EventError('No handler for event {}'.format(event.type))




    def content_item_create(self, event):
        pass





