# coding=utf-8
from sqlalchemy import Table, Column, Integer, Boolean, Float, String
from sqlalchemy.dialects.postgresql import UUID

from src.statistics.db.statmetadata import StatMetaData
from src.statistics.db.table.enum_coder_table_name import EnumCoderTableName

coder_table = Table(
    EnumCoderTableName.CODER.value,
    StatMetaData().metadata,
    Column('guid', UUID(as_uuid=True), primary_key=True),
    Column('coder_type', Integer),
    Column('coder_speed', Float),
    Column('input_length', Integer),
    Column('additional_length', Integer),
    Column('_interleaver', Boolean),
    Column('interleaver_length', Integer),
    Column('description', String(200))
)
