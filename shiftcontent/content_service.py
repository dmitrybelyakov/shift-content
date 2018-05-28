# todo: meta must be an object to be inheritable (do we need inheritance)
# todo: is content item an object as well?
# todo: if we are dealing with objects are we going full-orm?
# todo: is it a good idea to put custom meta fields into schema?
# todo: if we do that, can we go without ORM? <- that'd be perfect

# todo: orm is also makes graphql easier (but does it?)


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

    def create_item(self, content_type, author, data):
        pass

    def save_item(self, content_type, author, data):
        pass

    def delete_item(self, type, author, data):
        pass






