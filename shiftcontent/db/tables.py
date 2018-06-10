import sqlalchemy as sa


def define_tables(meta):
    """
    Creates content table definitions and adds them to schema catalogue.
    Use your application schema when integrating into your app for migrations
    support and other good things.

    :param meta: metadata catalogue to add to
    :return: dict
    """
    tables = dict()

    # events
    tables['events'] = sa.Table('content_events', meta,
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created', sa.DateTime, nullable=False, index=True),
        sa.Column('type', sa.String(256), nullable=False, index=True),
        sa.Column('author', sa.String(256), nullable=False, index=True),
        sa.Column('object_id', sa.Integer, nullable=False, index=True),
        sa.Column('payload', sa.Text),
    )

    # items projection
    # todo: object id
    # todo: path
    # todo: author
    # todo: object data

    # todo: version
    # todo: parent_version
    # todo: status

    # todo: lat
    # todo: long
    # todo: categories
    # todo: tags
    # todo: comments
    # todo: reactions [like]
    # todo: uvotes
    # todo: downvotes


    return tables

