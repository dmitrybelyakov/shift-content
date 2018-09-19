from .event_handlers import ContentItemCreate
from .event_handlers import ContentItemDelete
from .event_handlers import ContentItemUpdate
from .event_handlers import ContentItemFieldUpdateField
from .event_handlers import ContentItemSetParent

"""
Note: we used to have multiple chained handlers per event, but then decided to
have one handler do everything. It was starting to get a bit confusing. You can
still append your own handlers if you want to customize the behaviour.

@see: https://github.com/dmitrybelyakov/shift-content/issues/19
"""
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

    # update content item field
    CONTENT_ITEM_UPDATE_FIELD=[
        ContentItemFieldUpdateField,
    ],

    # set content item parent
    CONTENT_ITEM_SET_PARENT=[
        ContentItemSetParent
    ]
)


