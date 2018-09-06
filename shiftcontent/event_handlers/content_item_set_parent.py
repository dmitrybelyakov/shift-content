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
    """

    EVENT_TYPES = (
        'CONTENT_ITEM_SET_PARENT',
    )

    def handle(self, event):
        """
        Handle event
        Updates item path and all it's children paths.

        :param event: shiftcontent.events.event.Event
        :return: shiftcontent.events.event.Event
        """

        # get parent

        # get item

        # get item children

        # update item path

        # update children paths

        # put item to cache

        # put item to index

        # put children to cache

        # put children to index

        print('HANDLE SET PARENT EVENT')

        # and return
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
        print('ROLLBACK PARENT EVENT')
        return self.handle(event)





