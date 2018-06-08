

class EventService():
    """
    Event service
    Responsible for handling events
    """

    def __init__(self, db):
        """
        Init the service
        Requires an instance of database to work with events.
        :param db: shiftcontent.db.db.Db
        """
        self.db = db



    # todo: accept db instance
    # todo: validate and persist events
    # todo: dispatch events to event handlers
    # todo: event handlers must have access to db
    # todo: they will need to update projections
    # todo: build a simple projection for content item
