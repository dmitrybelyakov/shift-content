from mprop import mproperty

"""
Content services
Here we make use of the mprop library that implements module-level properties.
Each service is defined via such property to use delayed imports and allows
us to do imports without causing circular imports. You can easily do this 
without any issues:

  * from shiftcontent import services
  * from shiftcontent.services import events

"""

# created instances
_content = None
_db = None
_definition = None
_events = None


@mproperty
def content(mod):
    """
    Import and create content service
    :return: shiftcontent.content_service.ContentService
    """
    global _content
    if not _content:
        from shiftcontent.content_service import ContentService
        _content = ContentService()
    return _content


@mproperty
def db(mod):
    """
    Import and create database
    :return: shiftcontent.db.db.Db
    """
    global _db
    if not _db:
        from shiftcontent.db.db import Db
        _db = Db()
    return _db


@mproperty
def definition(mod):
    """
    Import and create definition service
    :return: shiftcontent.schema_service.SchemaService
    """
    global _definition
    if not _definition:
        from shiftcontent.schema_service import SchemaService
        _definition = SchemaService()
    return _definition


@mproperty
def events(mod):
    """
    Import and create event service
    :return: shiftevent.event_service.EventService
    """
    global _events
    if not _events:
        from shiftevent.event_service import EventService
        from shiftcontent.handlers import content_handlers
        _events = EventService(db=mod.db, handlers=content_handlers)
    return _events





