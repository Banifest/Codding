# coding=utf-8
from sqlalchemy import Table, Column, Integer, Boolean, Float, String
from sqlalchemy.dialects.postgresql import UUID

from src.statistics.db.table.statmetadata import StatMetaData

coder_table = Table(
    'coder',
    StatMetaData().get_metadata(),
    Column('guid', UUID, primary_key=True),
    Column('coder_type', Integer),
    Column('coder_speed', Float),
    Column('input_length', Integer),
    Column('additional_length', Integer),
    Column('interleaver', Boolean),
    Column('description', String(200))
)
