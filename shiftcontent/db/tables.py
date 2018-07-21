import sqlalchemy as sa
from pprint import pprint as pp
from shiftevent.db import define_tables as define_event_tables


def define_tables(meta):
    """
    Creates content table definitions and adds them to schema catalogue.
    Use your application schema when integrating into your app for migrations
    support and other good things.

    :param meta: metadata catalogue to add to
    :return: dict
    """

    # event store tables
    event_tables = define_event_tables(meta)

    # content tables
    content_tables = dict()
    content_tables['items'] = sa.Table('content_items', meta,
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created', sa.DateTime, nullable=False, index=True),
        sa.Column('type', sa.String(256), nullable=False, index=True),
        sa.Column('path', sa.String(256), nullable=True, index=True),
        sa.Column('author', sa.String(256), nullable=False, index=True),
        sa.Column('object_id', sa.String(256), nullable=False, index=True),
        sa.Column('data', sa.Text),
    )

    tables = {**content_tables, **event_tables}
    return tables

