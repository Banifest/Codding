# coding=utf-8
from sqlalchemy import Table, Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from statistics.db.table.statmetadata import StatMetaData

hamming_table = Table(
    'hamming',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True, ),
    Column('matrix', ARRAY(ARRAY(Boolean)))
)
