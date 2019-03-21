import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from shiftevent.db import define_tables as define_event_tables
from pprint import pprint as pp


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
    text = sa.Text()
    path_index = sa.Index('ix_content_items_path', 'path', unique=False)

    if dialect == 'mysql':
        text = mysql.LONGTEXT()
        path_index = sa.Index(
            'ix_content_items_path', 'path', unique=False, mysql_length=768
        )

    # content tables
    content_tables = dict()
    content_tables['items'] = sa.Table('content_items', meta,
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created', sa.DateTime, nullable=False, index=True),
        sa.Column('type', sa.String(256), nullable=False, index=True),
        sa.Column('path', text, nullable=True, unique=False),
        sa.Column('sort_order', sa.Integer, nullable=True, index=True),
        sa.Column('author', sa.String(256), nullable=False, index=True),
        sa.Column('object_id', sa.String(256), nullable=False, index=True),
        sa.Column('fields', text),
        path_index
    )

    tables = {**content_tables, **event_tables}
    return tables

