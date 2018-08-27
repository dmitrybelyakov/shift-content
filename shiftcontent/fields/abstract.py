
# TODO: do we define mapping separately (view, search)
# TODO: or do we encapsulate it in field type?

# TODO: whichever we choose we'll need sme processor to handle type conversions
# TODO: for each type so we can serialize-deserialize data from-to db/cache

# TODO: how do we store/process mapping for meta fields (view and search)?
# TODO: this should probably treated as a special case, e.g. meta geopoint

# TODO: can we do without field types instantiating lots of classes every time?

# TODO: what are the points at wich we need to do data conversions?

"""

VIEW MAPPING (python data types)

  * text
  * int
  * float
  * bool
  * date
  * datetime

DATABASE MAPPING (if not auto serializable to json)
  * date
  * datetime

SEARCH MAPPING (elasticsearch data types)
  * text
  * keyword
  * boolean
  * integer
  * long
  * float
  * double


"""


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