from shiftcontent.content_service import ContentService
from shiftcontent.schema_service import SchemaService
from shiftcontent.db.db import Db
from shiftevent.event_service import EventService
from shiftcontent.handlers import content_handlers

content = ContentService()
db = Db()
definition = SchemaService()
events = EventService(db=db, handlers=content_handlers)


