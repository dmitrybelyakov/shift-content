from uuid import uuid1
from pprint import pprint as pp
from shiftcontent import exceptions as x
from shiftcontent.item import Item
from shiftcontent.item_schema import CreateItemSchema, UpdateItemSchema
from shiftcontent.utils import import_by_name
from shiftcontent import db
from shiftcontent import definition_service
from shiftcontent import event_service
from shiftcontent import cache_service


class ContentService:
    """
    Content service is the main interface to content library. It works with
    projections to retrieve content, handles content updates via event
    service, monitors and updates in-memory caches and search indexes
    """
    def get_item(self, object_id):
        """
        Get item
        Selects an item from projection table by its unique object_id
        :param object_id: str, object id
        :return: shiftcontent.ite.Item
        """

        object_id = str(object_id)

        # try getting from cache first
        item = cache_service.get(object_id)
        if item:
            return item

        # get from projection table
        items = db.tables['items']
        with db.engine.begin() as conn:
            query = items.select().where(items.c.object_id == object_id)
            result = conn.execute(query).fetchone()
            if not result:
                return

        try:
            definition_service.get_type(result.type)
        except x.UndefinedContentType:
            msg = 'Database contains item ({}) of undefined type [{}]'
            raise x.UndefinedContentType(msg.format(result.id, result.type))

        # put to cache
        item = Item().from_db(result)
        cache_service.set(item)

        # and return
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
        type_definition = definition_service.get_type(content_type)

        for field in type_definition['fields']:
            filters = field['filters'] if 'filters' in field else ()
            validators = field['validators'] if 'validators' in field else ()
            if not filters and not validators:
                continue

            # add prop
            schema.add_property(field['handle'])
            prop = getattr(schema, field['handle'])

            # add custom filters
            for params in filters:
                params = {**params}  # copy, unfreeze
                filter_class = import_by_name(params['type'])
                del params['type']
                filter = filter_class(**params)
                prop.add_filter(filter)

            # add custom validators
            for params in field['validators']:
                params = {**params}  # copy, unfreeze
                validator_class = import_by_name(params['type'])
                del params['type']
                validator = validator_class(**params)
                prop.add_validator(validator)

        # and return
        return schema

    def create_item(self, author, content_type, fields, parent=None):
        """
        Create item
        Validates incoming data and returns validation errors. If data valid,
        emits a content item creation event and then after the handlers run,
        fetches the item by object_id

        :param author: str, author id
        :param content_type: str, content type
        :param fields: dict, content item fields
        :param parent: shiftcontent.item.Item, parent item
        :return: shiftcontent.itemItem
        """
        # drop nonexistent fields
        type_definition = definition_service.get_type(content_type)
        valid_fields = [field['handle'] for field in type_definition['fields']]
        fields = {f: v for f, v in fields.items() if f in valid_fields}

        object_id = str(uuid1())

        # validate data
        item_data = dict(
            type=content_type,
            author=author,
            object_id=object_id,
            **fields
        )

        context = dict(definition=definition_service.definition)
        schema = self.item_schema(content_type, 'create')
        result = schema.process(item_data, context)
        if not result:
            return result

        # create event
        event = event_service.event(
            type='CONTENT_ITEM_CREATE',
            author=author,
            object_id=object_id,
            payload=item_data
        )

        # and emit
        event = event_service.emit(event)

        # set parent if provided
        if parent:
            item = self.get_item(object_id)
            self.set_parent(author, item, parent)

        return self.get_item(event.object_id)

    def update_item(self, author, item):
        """
        Update item
        Accepts an item object validates it and tries to persist it. Will
        return validation errors if item is in invalid state, otherwise will
        emit an event.

        :param author: str, author id
        :param item: shiftcontent.item.Item, item object (must be saved first)
        :return: shiftcontent.item.Item
        """
        if not isinstance(item, Item):
            err = "Update function expects shiftcontent.item.Item, got [{}]"
            raise x.ItemError(err.format(type(item)))

        object_id = str(item.object_id)
        new_data = item.to_json()

        old_item = self.get_item(object_id) if object_id else None
        if not old_item:
            err = 'Item must be saved first to be updated. We were unable ' \
                  'to find item with such id [{}]'
            raise x.ItemNotFound(err.format(object_id))

        # validate
        context = dict(definition=definition_service.definition)
        schema = self.item_schema(item.type, schema_type='update')
        ok = schema.process(item, context=context)
        if not ok:
            return ok

        # prepare payload
        old_data = old_item.to_json()

        # create event
        event = event_service.event(
            type='CONTENT_ITEM_UPDATE',
            author=author,
            object_id=object_id,
            payload=new_data,
            payload_rollback=old_data
        )

        # emit
        event = event_service.emit(event)

        # update in place to reflect changes in clients
        updated = self.get_item(item.object_id)
        item.from_dict(updated.to_dict())

        return self.get_item(event.object_id)

    def update_item_field(self, author, object_id, field, value):
        """
        Update item field
        Updates single field on an item
        :param author: str, author id
        :param object_id: str, object id to update
        :param field: str, field name
        :param value: str, new value to set
        :return: shiftcontent.itemItem
        """
        item = self.get_item(object_id)
        if not item:
            err = 'Unable to find item with such id [{}]'
            raise x.ItemNotFound(err.format(object_id))

        if not item.is_updatable(field):
            err = 'Field [{}] is not allowed for content type [{}]'
            raise x.ItemError(err.format(field, item.type))

        # remember old value
        old_value = getattr(item, field)

        # validate
        setattr(item, field, value)
        context = dict(definition=definition_service.definition)
        schema = self.item_schema(item.type, schema_type='update')
        ok = schema.process(item, context=context)
        if not ok:
            return ok

        # is this a metafield?
        is_metafield = field in item.metafields

        # create event
        event = event_service.event(
            type='CONTENT_ITEM_UPDATE_FIELD',
            author=author,
            object_id=object_id,
            payload=dict(
                metafield=is_metafield,
                field=field,
                value=value
            ),
            payload_rollback=dict(
                metafield=is_metafield,
                field=field,
                value=old_value
            )
        )

        # emit
        event = event_service.emit(event)
        return self.get_item(event.object_id)

    def delete_item(self, author, object_id):
        """
        Delete content item
        Emits content deletion event.

        :param author: str or int, author id
        :param object_id: str, item object id to delete
        :return: shiftcontent.content_service.ContentService
        """
        item = self.get_item(object_id)
        if not item:
            err = 'Unable to delete nonexistent content item [{}]'
            raise x.ItemNotFound(err.format(object_id))

        rollback = item.to_json()

        # create event
        event = event_service.event(
            type='CONTENT_ITEM_DELETE',
            author=author,
            object_id=object_id,
            payload=None,
            payload_rollback=rollback
        )

        # emit
        event_service.emit(event)
        return self

    def set_parent(self, author, item, parent):
        """
        Set parent
        Sets item parent to allow nesting.

        :param author: str, author of this action
        :param item: shiftcontent.item.Item
        :param parent: shiftcontent.item.Item
        :return: shiftcontent.content_service.ContentService
        """
        if not item.id:
            err = 'Item must be saved first to get a parent of another item'
            raise x.ItemError(err)

        if not parent.id:
            err = 'Item must be saved first to become a parent of another item'
            raise x.ItemError(err)

        if item.id == parent.id:
            err = 'Unable to set item as a parent of itself'
            raise x.ItemError(err)

        if parent.path and str(item.object_id) in parent.path.split('.'):
            err = 'Unable to set parent as a child of its children'
            raise x.ItemError(err)

        previous_parent_id = item.path.split('.')[-1] if item.path else None
        new_parent_id = parent.object_id

        # create event
        event = event_service.event(
            type='CONTENT_ITEM_SET_PARENT',
            author=author,
            object_id=item.object_id,
            payload=dict(parent_object_id=new_parent_id),
            payload_rollback=dict(parent_object_id=previous_parent_id)
        )

        # emit
        event_service.emit(event)

        # update in place to reflect changes in clients
        updated = self.get_item(item.object_id)
        item.from_dict(updated.to_dict())

        return self

    def get_path(self, object_id):
        """
        Get path
        Returns a list of item object representing item ancestors.

        :param object_id: str, item object id
        :return: list or none
        """
        item = self.get_item(object_id)
        if not item or not item.path:
            return

        path = str(item.path).split('.')
        path = [self.get_item(object_id) for object_id in path]
        return path







