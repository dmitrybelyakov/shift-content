# from uuid import uuid1
# from pprint import pprint as pp
# from shiftcontent import exceptions as x
# from shiftcontent.item import Item
# from shiftcontent.item_schema import CreateItemSchema, UpdateItemSchema
# from shiftcontent.utils import import_by_name

from shiftcontent import services

class ContentService:
    """
    Content service is the main interface to content library. It works with
    projections to retrieve content, handles content updates via event
    service, monitors and updates in-memory caches and search indexes
    """
    def __init__(self):
        """
        Initialize content service
        Accepts an initialized database instance, event and schema services

        :param db: shiftcontent.db.db.Db - database instance
        :param event_service: shiftcontent.event_service.EventService
        :param schema_service: shiftcontent.schema_service.SchemaService
        """
        pass


    def get_item(self, object_id):
        """
        Get item
        Selects an item from projection table by its unique object_id
        :param object_id: str, object id
        :return: shiftcontent.ite.Item
        """
        # todo: try to get item from cache
        # todo: get from projections if not found
        # todo: put to cache if found in projections

        # get from projection table
        items = self.db.tables['items']
        with self.db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            if not result:
                return

            try:
                content_type = self.schema_service.get_type_schema(result.type)
            except x.UndefinedContentType:
                msg = 'Database contains item ({}) of undefined type [{}]'
                raise x.UndefinedContentType(msg.format(result.id, result.type))

            fields = [field['handle'] for field in content_type['fields']]
            item = Item(fields=fields, **dict(result))
            return item

    def item_schema(self, content_type, schema_type='update'):
        """
        Creates item filtering and validation schema from content type
        definition. The schema type can either be 'create' or 'update' where
        the latter will additionally test for item id being present.

        :param content_type: str, content type
        :param schema_type: str, create or update
        :return: shiftschema.schema.Schema
        """

        # check schema type
        schema_types = dict(
            create=CreateItemSchema,
            update=UpdateItemSchema
        )

        if schema_type not in schema_types:
            err = 'Invalid schema type [{}]. Must be "create" or "update"'
            raise x.InvalidItemSchemaType(err.format(schema_type))

        # default schema
        schema = schema_types[schema_type]()

        # add filter/validators defined in schema
        definition = self.schema_service.get_type_schema(content_type)
        for field in definition['fields']:
            filters = field['filters'] if field['filters'] else ()
            validators = field['validators'] if field['validators'] else ()
            if not filters and not validators:
                continue

            # add prop
            schema.add_property(field['handle'])
            prop = getattr(schema, field['handle'])

            # add custom filters
            for params in filters:
                filter_class = import_by_name(params['type'])
                del params['type']
                filter = filter_class(**params)
                prop.add_filter(filter)

            # add custom validators
            for params in field['validators']:
                validator_class = import_by_name(params['type'])
                del params['type']
                validator = validator_class(**params)
                prop.add_validator(validator)

        # and return
        return schema

    def create_item(self, author, content_type, data, parent=None):
        """
        Create item
        Validates incoming data and returns validation errors. If data valid,
        emits a content item creation event and then after the handlers run,
        fetches the item by object_id

        :param author: str, author id
        :param content_type: str, content type
        :param data: dict, content item fields
        :param parent: shiftcontent.item.Item, parent item
        :return:
        """
        # drop nonexistent fields
        type_definition = self.schema_service.get_type_schema(content_type)
        valid_fields = [field['handle'] for field in type_definition['fields']]
        fields = {f: v for f, v in data.items() if f in valid_fields}

        # validate data
        item_data = dict(
            type=content_type,
            author=author,
            object_id=str(uuid1()),
            **fields
        )

        context = dict(definition=self.schema_service.schema)
        schema = self.item_schema(content_type, 'create')
        result = schema.process(item_data, context)
        if result is False:
            return result

        # # create event
        event = self.event_service.event(
            author=author,
            object_id=item_data['object_id'],
            type='CONTENT_ITEM_CREATE',
            payload=item_data
        )

        # and emit
        event = self.event_service.emit(event)
        return self.get_item(event.object_id)

        # todo: who's responsibility is it to update caches?
        # todo: content service or event handler? - not content service!
        # todo: time travelling should also update caches

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

    def save_item(self, content_type, author, data):
        pass

    def delete_item(self, type, author, data):
        pass






