[![Build Status](https://api.travis-ci.org/dmitrybelyakov/shift-content.svg?branch=master)](https://travis-ci.org/dmitrybelyakov/shift-content)
[![Coverage Status](https://coveralls.io/repos/github/dmitrybelyakov/shift-content/badge.svg?branch=master)](https://coveralls.io/github/dmitrybelyakov/shift-content?branch=master)

# shift-content
Lightweight headless CMF. Not ready for use yet.

## Configuration

### Manually configure 

Shiftcontent provides several global services that use delayed instantiation. So in your app, you import the services and call `init()` method on the services to pass in your config parameters. It is recomended to do this as early as possible, preferably right alter or at import time. Here is an example such instantiation:

```python
import shiftcontent

# init database
shiftcontent.db.init(
    engine=engine,
    db_url='mysql://', # either url or engine,
    meta=None,         # use custom metadata
    dialect='mysql',   # only required for mysql,
    **db_params={}     # additional db engine params
)

# init definitions
shiftcontent.definition_service.init(
    definition_path='./path/to/definition/file.yml',
    revisions_path='./path/to/revisions/directory/'
)    

# init cache (optional)
shiftcontent.cache_service.init(
    cache_name='content',  # cache name/key prefix
    default_ttl=2628000,   # default ttl (a month)
    host='localhost',      # redis host
    port=6379,             # redis port
    db=1,                  # redis db
    **redis_params         # additional redis parameters
)

#  init search (optional)
shiftcontent.search_service.init(
    hosts=('localhost:9200', ),  # elasticsearch nodes
    index_name='content',        # index name
    doc_type='content',          # document type
    sniff=True,                  # sniff nodes
    **elasticsearch_params       # additional elasticsearch params
)
```

### Integration with flask

In addition to manual initialization we provide feature function that accepts an instance of flask app and initializes services from flask app config. Wherever you create your flask app or have access to `app`, enable it like so:

```python
from shiftcontent.boiler import content_feature
content_feature(app)
```

This will look for the following variables in flask config:

| Setting | Required | Default | Description |
|---|---|---|---|
| **SHIFTCONTENT_DB_URL** | URL or engine required | `None` | SqlAlchemy DB URL |
| **SHIFTCONTENT_DB_ENGINE** | URL or engine required | `None` | Instance of sqlalchemy database engine |
| **SHIFTCONTENT_DB_META** | No | `None` | Custom metadata object |
| **SHIFTCONTENT_DB_DIALECT** | Required for mysql | `None` | Dialect name, has to be set for mysql to `mysql` |
| **SHIFTCONTENT_DB_PARAMS** | No | `None` | Additional params for sqlalchemy engine. Only works with db_url |
| **SHIFTCONTENT_DEFINITION** | Yes | `None` | Path to content types definition yaml file |
| **SHIFTCONTENT_REVISIONS** | Yes | `No` | Path to directory for definition revisions (required) |
| **SHIFTCONTENT_CACHE_SUPPORT** | No | `None` | Whether to enable caching |
| **SHIFTCONTENT_CACHE_NAME** | No | `content` | Cache name |
| **SHIFTCONTENT_CACHE_TTL** | No | `2628000` | Default TTL for caches, defaults to a month |
| **SHIFTCONTENT_CACHE_HOST** | No | `localhost` | Redis host |
| **SHIFTCONTENT_CACHE_PORT** | No | `6379` | Redis port |
| **SHIFTCONTENT_CACHE_DB** | No | `1` | Redis DB |
| **SHIFTCONTENT_CACHE_PARAMS** | No | `{}` | Additional redis parameters |
| **SHIFTCONTENT_SEARCH_SUPPORT** | No | `None` | Whether to enable searching |
| **SHIFTCONTENT_SEARCH_HOSTS** | No | `('localhost:9200', )` | List of elasticsearch nodes |
| **SHIFTCONTENT_SEARCH_INDEX** | No | `content` | Index name |
| **SHIFTCONTENT_SEARCH_DOC_TYPE** | No | `content` | Document type |
| **SHIFTCONTENT_SEARCH_SNIFF** | No | `True` | Sniff elastic search and form a cluster|
| **SHIFTCONTENT_SEARCH_PARAMS** | No | `{}` | Additional elasticsearch params |




### MySQL: Explicitly define a dialect

**Note:** this is not required for other database engines like PostgreSQL, or SQLite.

Because mysql has a limited size `TEXT` column that becomes event smaller if you use UTF8 multi-byte (see mysql unicode issues in troubleshooting section) it is sometimes not enough to to storer large articles.

For this reason you have to explicitly tel shiftcontent tables that you are using MySQL, so it can switch column type to mysql-specific `LONGTEXT` format:


```python
from shiftcontent import db

db.init(db_url='...', dialect='mysql')
```

To integrate with Alembic migrations, update your `migrations/env.py` file to include:

```python
from shiftcontent.database import define_tables

define_tables(context.config.meta, dialect='mysql')
```



## Troubleshooting


### Mysql Unicode Issues

You might run into issues when trying to insert unicode content like this:
```
I can do smilies! 😀
```

Results in an error similar to this:

```
sqlalchemy.exc.OperationalError: (_mysql_exceptions.OperationalError) (1366, 'Incorrect string value: \'\\xF0\\x9F\\x98\\x80"}\'
```

Please make sure your database and python driver are bot set to use `utf8mb4`.
