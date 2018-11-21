# coding=utf-8
from sqlalchemy import Table, Column, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID

from statistics.db.table.statmetadata import StatMetaData

result_table = Table(
    'test_result',
    StatMetaData().get_metadata(),
    Column('timestamp', UUID, primary_key=True),
    Column('flg_cascade', Boolean),
    Column('first_coder', UUID),
    Column('second_coder', UUID),
    Column('type_of_noise', Integer),
    Column('type_of_noise', Float)
)