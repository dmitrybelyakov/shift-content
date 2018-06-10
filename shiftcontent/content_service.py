from uuid import uuid1


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

    def get_item(self, item_id):
        # todo: try to get item from cache
        # todo: get from projections if not found
        # todo: put to cache if found in projections
        pass

    def create_item(self, content_type, author, data):
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
        pass

    def save_item(self, content_type, author, data):
        pass

    def delete_item(self, type, author, data):
        pass






