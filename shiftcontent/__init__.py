
"""
Initialize content services
All the services use delayed initialization so that users can inject their
settings later, but we still have these services globally importable.

The order of definition is important here so that we don't run into circular
dependencies, so the services with no dependencies are created here first.
"""


# init database (no dependencies)
from .database.db import Db
db = Db()

# init cache service
from shiftmemory import Memory
cache_service = Memory()

# init schema (no dependencies)
from .definition_service import DefinitionService
definition_service = DefinitionService()


# init search service
from .search_service import SearchService
search_service = SearchService()

# init events (needs db)
from shiftevent.event_service import EventService
from shiftcontent.handlers import content_handlers
event_service = EventService(db=db, handlers=content_handlers)

# init content (needs db and events)
from .content_service import ContentService
content_service = ContentService()


