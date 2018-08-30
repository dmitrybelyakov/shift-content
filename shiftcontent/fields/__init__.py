from .text import Text
from .boolean import Boolean
from .date import Date
from .datetime import DateTime
from .datetime_meta import DateTimeMetaField
from .integer import Integer
from .float import Float
from .geopoint_meta import GeopointMeta

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