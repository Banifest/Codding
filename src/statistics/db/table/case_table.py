# coding=utf-8

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from src.statistics.db.statmetadata import StatMetaData
from src.statistics.db.table.enum_coder_table_name import EnumCoderTableName

case_table = Table(
    EnumCoderTableName.CASE_RESULT.value,
    StatMetaData().metadata,
    Column('guid', UUID(as_uuid=True), primary_key=True),
    Column('test_timestamp', TIMESTAMP, ForeignKey("test_result.timestamp")),
    Column('count_correct_bits', Integer),
    Column('count_incorrect_bits', Integer),
    Column('count_repair_bits', Integer),
    Column('count_changed_bits', Integer)
)
