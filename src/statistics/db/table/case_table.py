# coding=utf-8
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from src.statistics.db.table.statmetadata import StatMetaData

case_table = Table(
    'case_result',
    StatMetaData().get_metadata(),
    Column('guid', UUID, primary_key=True),
    Column('test_timestamp', TIMESTAMP, ForeignKey("test_result.timestamp")),
    Column('count_correct_bits', Integer),
    Column('count_incorrect_bits', Integer),
    Column('count_repair_bits', Integer),
    Column('count_changed_bits', Integer)
)
