from .handlers import Dummy1
from .handlers import Dummy2
from .handlers import ContentItemCreate

default_handlers = dict(

    # dummy handlers
    DUMMY_EVENT=[
        Dummy1,
        Dummy2
    ],

    # create content item
    CONTENT_ITEM_CREATE=[
        ContentItemCreate
    ]
)