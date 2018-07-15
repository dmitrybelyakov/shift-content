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

    # items
    tables['items'] = sa.Table('content_items', meta,
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created', sa.DateTime, nullable=False, index=True),
        sa.Column('type', sa.String(256), nullable=False, index=True),
        sa.Column('path', sa.String(256), nullable=True, index=True),
        sa.Column('author', sa.String(256), nullable=False, index=True),
        sa.Column('object_id', sa.String(256), nullable=False, index=True),
        sa.Column('data', sa.Text),
    )

    return tables

