import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from pprint import pprint as pp
from shiftevent.db import define_tables as define_event_tables


def define_tables(meta, dialect=None):
    """
    Creates content table definitions and adds them to schema catalogue.
    Use your application schema when integrating into your app for migrations
    support and other good things.

    :param meta: metadata catalogue to add to
    :param dialect: str, sql dialect, optional but required for mysql
    :return: dict
    """

    # event store tables
    event_tables = define_event_tables(meta, dialect=dialect)

    # mysql dialect requires longtext column for fields
    fields_type = sa.Text() if dialect != 'mysql' else mysql.LONGTEXT()

    # content tables
    content_tables = dict()
    content_tables['items'] = sa.Table('content_items', meta,
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created', sa.DateTime, nullable=False, index=True),
        sa.Column('type', sa.String(256), nullable=False, index=True),
        sa.Column('path', sa.String(256), nullable=True, index=True),
        sa.Column('author', sa.String(256), nullable=False, index=True),
        sa.Column('object_id', sa.String(256), nullable=False, index=True),
        sa.Column('fields', fields_type),
    )

    tables = {**content_tables, **event_tables}
    return tables

