from .event_handlers import ContentItemCreate
from .event_handlers import ContentItemDelete
from .event_handlers import ContentItemUpdate
from .event_handlers import ContentItemFieldUpdateField

content_handlers = dict(

    # create content item
    CONTENT_ITEM_CREATE=[
        ContentItemCreate
    ],

    # delete content item
    CONTENT_ITEM_DELETE=[
        ContentItemDelete
    ],

    # update content item
    CONTENT_ITEM_UPDATE=[
        ContentItemUpdate
    ],
    # update content item
    CONTENT_ITEM_UPDATE_FIELD=[
        ContentItemFieldUpdateField
    ],
)


