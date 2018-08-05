from .event_handlers import ContentItemCreate
from .event_handlers import ContentItemDelete
from .event_handlers import ContentItemUpdate
from .event_handlers import ContentItemFieldUpdateField
from .event_handlers import ContentItemIndex
from .event_handlers import ContentItemRemoveFromIndex
from .event_handlers import ContentItemCache
from .event_handlers import ContentItemRemoveFromCache

content_handlers = dict(

    # create content item
    CONTENT_ITEM_CREATE=[
        ContentItemCreate,
        ContentItemIndex,
        ContentItemCache
    ],

    # delete content item
    CONTENT_ITEM_DELETE=[
        ContentItemDelete,
        ContentItemRemoveFromIndex,
        ContentItemRemoveFromCache
    ],

    # update content item
    CONTENT_ITEM_UPDATE=[
        ContentItemUpdate,
        ContentItemIndex,
        ContentItemCache
    ],
    # update content item
    CONTENT_ITEM_UPDATE_FIELD=[
        ContentItemFieldUpdateField,
        ContentItemIndex,
        ContentItemCache
    ],
)


