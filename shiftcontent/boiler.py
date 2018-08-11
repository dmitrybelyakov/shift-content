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
    from boiler.feature.orm import db

    with app.app_context():
        engine = db.engine

    # get flask config
    cfg = app.config

    # init db (required)
    shiftcontent.db.init(engine=engine)

    # init definition config
    cwd = os.getcwd()
    shiftcontent.definition_service.init(
        definition_path=os.path.join(cwd, 'tests', '_assets', 'content.yml'),
        revisions_path=os.path.join(cwd, 'var', 'data', 'content_revisions')
    )

    # init cache
    if cfg.get('SHIFTCONTENT_CACHE_SUPPORT'):
        shiftcontent.cache_service.init(
            cache_name='content_items_search',
            host='localhost',
            port=6379,
            db=1,
            params={
                'query': {
                    'match_phrase': {
                        'full_text': 'horror'
                    }
                }
            }
        )

    # init search
    if cfg.get('SHIFTCONTENT_SEARCH_SUPPORT'):
        shiftcontent.search_service.init(
            hosts=('localhost:9200', ),
            index_name='content',
            doc_type='content',
            # params=dict()
        )


