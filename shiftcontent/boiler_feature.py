import os
from boiler.feature.orm import db
import shiftcontent


def content_feature(app):
    """
    Content feature
    Provides integration with shiftboiler template flask app: receives a
    flask app and initializes global content services from flask app config.

    :param app: flask.Flask
    :return: None
    """
    # get flask config
    cfg = app.config

    # get engine from boiler
    engine = None
    try:
        from boiler.feature.orm import db
        with app.app_context():
            engine = db.engine
    except ImportError:
        engine = cfg.get('SHIFTCONTENT_DB_ENGINE')

    # init db (required)
    db_params = dict(
        meta=cfg.get('SHIFTCONTENT_DB_META'),
        dialect=cfg.get('SHIFTCONTENT_DB_DIALECT'),
        **cfg.get('SHIFTCONTENT_DB_PARAMS', {})
    )
    if engine:
        db_params['engine'] = engine
    else:
        db_params['db_url'] = cfg.get('SHIFTCONTENT_DB_URL')

    shiftcontent.db.init(**db_params)

    # init definition config
    shiftcontent.definition_service.init(
        definition_path=cfg.get('SHIFTCONTENT_DEFINITION'),
        revisions_path=cfg.get('SHIFTCONTENT_REVISIONS')
    )

    # init cache
    if cfg.get('SHIFTCONTENT_CACHE_SUPPORT'):
        shiftcontent.cache_service.init(
            cache_name=cfg.get('SHIFTCONTENT_CACHE_NAME', 'content'),
            default_ttl=cfg.get('SHIFTCONTENT_CACHE_TTL', 2628000),
            host=cfg.get('SHIFTCONTENT_CACHE_HOST', 'localhost'),
            port=cfg.get('SHIFTCONTENT_CACHE_PORT', 6379),
            db=cfg.get('SHIFTCONTENT_CACHE_DB', 1),
            **cfg.get('SHIFTCONTENT_CACHE_PARAMS', {})
        )

    # init search
    if cfg.get('SHIFTCONTENT_SEARCH_SUPPORT'):
        shiftcontent.search_service.init(
            hosts=cfg.get('SHIFTCONTENT_SEARCH_HOSTS', ('localhost:9200', )),
            index_prefix=cfg.get('SHIFTCONTENT_SEARCH_INDEX_PREFIX'),
            doc_type=cfg.get('SHIFTCONTENT_SEARCH_DOC_TYPE', 'content'),
            sniff=cfg.get('SHIFTCONTENT_SEARCH_SNIFF', True),
            **cfg.get('SHIFTCONTENT_SEARCH_PARAMS', {})
        )


