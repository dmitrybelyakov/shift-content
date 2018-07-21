from shiftschema.schema import Schema
from shiftschema import filters
from shiftschema import validators

from shiftcontent.validators import TypeExists


class BaseItemSchema(Schema):
    """
    Base content item schema
    By default contains only contains rules for item meta fields. Typically
    it would be created by a factory method in content service, that will
    attach additional validators and filters based on content type definition.
    """
    def schema(self):

        # item id
        self.add_property('id')
        self.id.add_validator(validators.Required(
            message='Content item requires an id'
        ))

        # item author
        self.add_property('author')
        self.author.add_validator(validators.Required(
            message='Content item requires an author'
        ))

        # content type
        self.add_property('type')
        self.type.add_validator(TypeExists())
        self.type.add_validator(validators.Required(
            message='Content item must have content type defined'
        ))

        # object id
        self.add_property('object_id')
        self.object_id.add_validator(validators.Required(
            message='Content item must have an object id'
        ))



