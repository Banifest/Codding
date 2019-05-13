# coding=utf-8
from sqlalchemy import Table, Column, Integer, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from src.statistics.db.table.enum_coder_table_name import EnumCoderTableName
from src.statistics.db.table.statmetadata import StatMetaData

result_table = Table(
    EnumCoderTableName.TEST_RESULT.value,
    StatMetaData().metadata,
    Column('timestamp', TIMESTAMP, primary_key=True),
    Column('flg_cascade', Boolean),
    Column('first_coder', UUID(as_uuid=True), ForeignKey("coder.guid")),
    Column('second_coder', UUID(as_uuid=True), ForeignKey("coder.guid")),
    Column('type_of_noise', Integer),
    Column('noise', Float)
)
