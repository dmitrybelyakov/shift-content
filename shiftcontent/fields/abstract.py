

class AbstractFieldType():
    """
    Abstract field type
    Defines the interface your concrete field types must implement.
    A field type is used to do data conversions from the data stored to various
    representation, like json, search etc. This is how you can tell certain
    fields to be of specific data types whn put to index or cache, or loaded
    back into your application.
    """
    pass