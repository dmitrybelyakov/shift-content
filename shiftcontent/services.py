from shiftcontent.content_service import ContentService
from shiftcontent.schema_service import SchemaService
from shiftcontent.db.db import Db

content = ContentService()
db = Db('sqlite://')
definition = SchemaService('123', '456')


