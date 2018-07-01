from uuid import uuid1
from pprint import pprint as pp
from shiftcontent import exceptions as x


class ContentService:
    """
    Content service is the main interface to content library. It works with
    projections to retrieve content, handles content updates via event
    service, monitors and updates in-memory caches and search indexes
    """
    def __init__(self, db, event_service, schema_service):
        """
        Initialize content service
        Accepts an initialized database instance, event and schema services

        :param db: shiftcontent.db.db.Db - database instance
        :param event_service: shiftcontent.event_service.EventService
        :param schema_service: shiftcontent.schema_service.SchemaService
        """
        self.db = db
        self.event_service = event_service
        self.schema_service = schema_service

    def get_item(self, object_id):
        # todo: try to get item from cache
        # todo: get from projections if not found
        # todo: put to cache if found in projections
        pass

    def create_item(self, author, content_type, data, parent=None):

        # create event
        type = self.schema_service.get_type_schema(content_type)
        valid = [field['handle'] for field in type['fields']]
        fields = {f: v for f, v in data.items() if f in valid}
        event = self.event_service.event(
            author=author,
            object_id=uuid1(),
            type='CONTENT_ITEM_CREATE',
            payload=dict(type=content_type, data=fields)
        )

        # and emit
        item = self.event_service.emit(event)
        return item

        # todo: who's responsibility is it to update caches?
        # todo: content service or event handler?


        # todo: filter and validate data
        # todo: send event
        # todo: what happens after an event is recorded?
        # todo: a projection should update
        # todo: cache should be refreshed
        # todo: we return item from the cache

        # todo: who updates projections?
        # todo: how events are replayed?
        # todo: we replay by sequentially firing events
        # todo: then handlers get executed to perform actions on db
        # todo: are event handlers async?
        # todo: if we are how can we return an item here? and do we?
        # todo: or should we just return an id here?

    def save_item(self, content_type, author, data):
        pass

    def delete_item(self, type, author, data):
        pass






