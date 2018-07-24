from mprop import mproperty

from .db.db import Db
db = Db()

from .schema_service import SchemaService
definition = SchemaService()

from .content_service import ContentService
content = ContentService()



from shiftevent.event_service import EventService
from .handlers import content_handlers
events = EventService(db=db, handlers=content_handlers)

