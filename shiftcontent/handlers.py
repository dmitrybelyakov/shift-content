from .event_handlers import ContentItemCreate
from .event_handlers import ContentItemDelete

content_handlers = dict(

    # create content item
    CONTENT_ITEM_CREATE=[
        ContentItemCreate
    ],

    # delete content item
    CONTENT_ITEM_DELETE=[
        ContentItemDelete
    ]
)