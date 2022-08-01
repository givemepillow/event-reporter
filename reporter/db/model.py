from sqlalchemy import (
    Column,
    MetaData, Table, DateTime, func, Index, Integer,
)

from sqlalchemy.dialects.postgresql import UUID

convention = {
    'all_column_names': lambda constraint, table: ''.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix%(table_name)s%(all_column_names)s',
    'uq': 'uq%(table_name)s%(all_column_names)s',
    'ck': 'ck%(table_name)s%(constraint_name)s',
    'fk': 'fk%(table_name)s%(all_column_names)s%(referred_table_name)s',
    'pk': 'pk%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

recipients = Table(
    'urls', metadata,
    Column('chat_id', Integer, primary_key=True),
    Column('token', UUID(as_uuid=True), nullable=False, unique=True),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now()),
    Index('idx_token', 'token', unique=True),
)
