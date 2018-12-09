# coding=utf-8
from sqlalchemy import Table, Column, Boolean, ForeignKey, Integer, BigInteger
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from src.statistics.db.table.statmetadata import StatMetaData

hamming_table = Table(
    'hamming',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    # array[][]
    Column('matrix', ARRAY(Boolean))
)

cyclic_table = Table(
    'cyclic',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    # array[][]
    Column('matrix_g', ARRAY(BigInteger)),
    # array[][]
    Column('matrix_h', ARRAY(BigInteger)),
    Column('polynomial', ARRAY(Integer))
)

fountain_table = Table(
    'fountain',
    StatMetaData().get_metadata(),
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('count_info_block', Integer),
    Column('count_block', Integer),
    Column('block_size', Integer),
    # array[][]
    Column('block_array', ARRAY(BigInteger))
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
