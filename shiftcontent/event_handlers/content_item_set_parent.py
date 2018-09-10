from shiftevent.handlers.base import BaseHandler
from shiftcontent.item import Item
from shiftcontent import db
from shiftcontent import cache_service
from shiftcontent import search_service
from shiftmemory import exceptions as cx
from pprint import pprint as pp


class ContentItemSetParent(BaseHandler):
    """
    Set parent
    Makes one content item parent of another and updates all item's children
    accordingly modifying their paths. The event is only reflected in the
    item getting a parent, so nested children will not get this event in their
    log and can be individually rewound.

    Expects the following payload structure:
    event = {
        ...
        payload={parent_object_id='d2bf6e2c-aba6-11e8-89e5'},
        payload_rollback={parent_object_id='d34c100c-aba6-11e8-89e5},
    }

    """

    EVENT_TYPES = (
        'CONTENT_ITEM_SET_PARENT',
    )

    def set_parent(self, item_object_id, parent_object_id=None):
        """
        Set parent
        Allows to set parent on an item or drop it by setting it to None (which
        will make an item root-level). This gets used both in handle and
        rollback functions as they are essentially the same.

        :param item_object_id: str, object id of an item to set parent on
        :param parent_object_id: str, object id of the parent object
        :return:
        """
        items = db.tables['items']
        with db.engine.begin() as conn:

            # get parent
            parent = None
            if parent_object_id:
                query = items.select().where(
                    items.c.object_id == parent_object_id
                )
                data = conn.execute(query).fetchone()
                if not data:  # pragma: no cover
                    return

                parent = Item()
                parent.from_db(data)

            # get item
            query = items.select().where(items.c.object_id == item_object_id)
            data = conn.execute(query).fetchone()
            if not data:  # pragma: no cover
                return

            item = Item()
            item.from_db(data)

            # get item children
            children = []
            if item.object_id:
                if item.path:
                    like = '{}.{}%'.format(item.path, item.object_id)
                else:
                    like = '{}%'.format(str(item.object_id))
                query = items.select().where(items.c.path.like(like))
                data = conn.execute(query).fetchall() or ()
                children = [Item().from_db(child) for child in data]

            # update item path
            if not parent:
                path = None
            elif parent.path:
                path = '{}.{}'.format(parent.path, parent.object_id)
            else:
                path = str(parent.object_id)

            query = items.update().where(items.c.object_id == item_object_id)
            conn.execute(query.values(dict(path=path)))
            item.path = path

            # update children paths
            for child in children:
                if item.path:
                    update = '{}.{}'.format(
                        item.path,
                        item.object_id
                    ).split('.')
                else:
                    update = [str(item.object_id)]

                child_path = child.path.split('.')
                index = child_path.index(str(item.object_id))
                path = '.'.join(update + child_path[index+1:])

                where = items.c.object_id == child.object_id
                query = items.update().where(where)
                conn.execute(query.values(dict(path=path)))
                child.path = path

        # put item to cache & index
        cache_service.set(item)
        search_service.put_to_index(item)

        # put children to cache & index
        for child in children:
            cache_service.set(child)
            search_service.put_to_index(child)

        return

    def handle(self, event):
        """
        Handle event
        Updates item path and all it's children paths.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        self.set_parent(
            item_object_id=event.object_id,
            parent_object_id=event.payload['parent_object_id']
        )

        return event

    def rollback(self, event):
        """
        Rollback event
        Resets items path from rollback payload if it has a previous parent id,
        otherwise sets item to have no parent (root items) and updates all
        item's children accordingly.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """
        self.set_parent(
            item_object_id=event.object_id,
            parent_object_id=event.payload_rollback['parent_object_id']
        )

        return event





