








class ContentType():
    pass

class ContentMeta():

    # todo: meta must be an object to be inheritable
    # todo: is content item an object as well?
    # todo: if we are dealing with objects are we going full-orm?
    # todo: is it a good idea to put custom meta fields into schema?
    # todo: if we do that, can we go without ORM? <- that'd be perfect

    id = None
    parent = None
    children = []
    fields = {
        'title': None,
        'description': None,
        'keywords': None
    }

    def __init__(self):
        self.fields['title'] = ''

    def to_dict(self):
        return dict(
            id=self.id,

        )


class ContentItem:
    id = None
    type = None
    version = None
    meta = ContentMeta()
    fields = {
        'handle': 'value'
    }

    # todo: content item must be serializable and de-serializable







class ContentService:
    pass






