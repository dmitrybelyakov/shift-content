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

    # employees
    tables['employees'] = sa.Table('employees', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(128)),
        sa.Column('full_name', sa.String(128)),
    )

    # addresses
    tables['addresses'] = sa.Table('addresses', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', None, sa.ForeignKey('employees.id')),
        sa.Column('email_address', sa.String(256), nullable=False)
    )

    return tables

