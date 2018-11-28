# coding=utf-8
from sqlalchemy import Table, Column, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from statistics.db.table.statmetadata import StatMetaData

hamming_table = Table(
    'hamming',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('matrix', ARRAY(ARRAY(Boolean)))
)

cyclic_table = Table(
    'cyclic',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('matrix_g', ARRAY(ARRAY(Boolean))),
    Column('matrix_h', ARRAY(ARRAY(Boolean))),
    Column('polynomial', ARRAY(Integer))
)

fountain_table = Table(
    'fountain',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('count_info_block', Integer),
    Column('count_block', Integer),
    Column('block_size', Integer),
    Column('block_array', ARRAY(ARRAY(Integer)))
)

convolution_table = Table(
    'convolution',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('count_polynomial', Integer),
    Column('count_input_bits', Integer),
    Column('count_output_bits', Integer),
    Column('count_registers', Integer)
)
