from shiftcontent.events.event import Event, EventSchema
from shiftcontent.item import Item
from shiftcontent import exceptions as x


class EventService:
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

    @property
    def handlers(self):
        """
        Event handlers
        Returns a dictionary of event handlers
        :return: dict
        """
        handlers = dict(
            DUMMY_EVENT=[self.dummy_event1, self.dummy_event2],
            CONTENT_ITEM_CREATE=[self.content_item_create]
        )

        return handlers

    def event(self, type, object_id, author, payload):
        """
        Persist an event
        Creates a new event object, validates it and saves to the database.
        May throw a validation exception if some event data is invalid.

        :param type: str, event type
        :param object_id: str, an id of the object being affected
        :param author:  str, author id in external system
        :param payload: dict, event payload
        :return: shiftcontent.event.Event
        """
        # create
        event = Event(
            type=type,
            author=author,
            object_id=object_id,
            payload=payload
        )

        # check handler presence
        if type not in self.handlers:
            msg = 'No handlers for event of type [{}]'
            raise x.EventError(msg.format(type))

        # validate
        schema = EventSchema()
        ok = schema.process(event)
        if not ok:
            raise x.InvalidEvent(validation_errors=ok.get_messages())

        # and save
        events = self.db.tables['events']
        with self.db.engine.begin() as conn:
            data = event.to_db()
            del data['id']
            result = conn.execute(events.insert(), **data)
            event.id = result.inserted_primary_key[0]

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

        # todo: move me to base handler
        if not event.id:
            raise x.EventError('To emit an event it must be saved first')

        # get handlers
        if event.type not in self.handlers:
            raise x.EventError('No handlers for event {}'.format(event.type))

        # trigger handlers
        handlers = self.handlers[event.type]
        for handler in handlers:
            event = handler(event, self.db)
        return event

    def get_event(self, id):
        """
        Get event
        Returns event found by unique id.
        :param id: int, event id
        :return: shiftcontent.event.Event
        """
        event = None
        events = self.db.tables['events']
        with self.db.engine.begin() as conn:
            select = events.select().where(events.c.id == id)
            data = conn.execute(select).fetchone()
            if data:
                event = Event(**data)
        return event

    # --------------------------------------------------------------------------
    # handlers
    # --------------------------------------------------------------------------

    # todo: events should be external
    # todo: think of a handler interface
    # todo: allow to chain handlers
    # todo: allow to add handlers from userland code
    # todo: how to roll back single event without replaying the whole store?

    def dummy_event1(self, event, db):
        """
        Dummy event handler 1
        Used for testing. In reality we should never modify an event.
        :param event: shiftcontent.event.Event
        :param db: shiftcontent.db.db.Db
        :return:
        """
        payload = event.payload
        payload['dummy_handler1'] = 'processed'
        event.payload = payload
        return event

    def dummy_event2(self, event, db):
        """
        Dummy event handler 2
        Used for testing. In reality we should never modify an event.
        :param event: shiftcontent.event.Event
        :param db: shiftcontent.db.db.Db
        :return:
        """
        payload = event.payload
        payload['dummy_handler2'] = 'processed'
        event.payload = payload
        return event

    def content_item_create(self, event, db):
        """
        Create content item
        :param event:
        :param db: shiftcontent.db.db.Db
        :return:
        """

        # create item
        item = Item(
            author=event.author,
            object_id=event.object_id,
            type=event.payload['type'],
            data=event.payload['data']
        )

        # persist
        items = db.tables['items']
        with self.db.engine.begin() as conn:
            result = conn.execute(items.insert(), **item.to_db())
            item.id = result.inserted_primary_key[0]

        # and return
        return item







