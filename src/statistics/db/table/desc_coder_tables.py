# coding=utf-8
from sqlalchemy import Table, Column, Boolean, ForeignKey, Integer, BigInteger
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from src.statistics.db.table.enum_coder_table_name import EnumCoderTableName
from src.statistics.db.table.statmetadata import StatMetaData

hamming_table = Table(
    EnumCoderTableName.HAMMING.value,
    StatMetaData().metadata,
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    # array[][]
    Column('matrix', ARRAY(Boolean))
)

cyclic_table = Table(
    EnumCoderTableName.CYCLIC.value,
    StatMetaData().metadata,
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    # array[][]
    Column('matrix_g', ARRAY(BigInteger)),
    # array[][]
    Column('matrix_h', ARRAY(BigInteger)),
    Column('_polynomial', ARRAY(Integer))
)

fountain_table = Table(
    EnumCoderTableName.FOUNTAIN.value,
    StatMetaData().metadata,
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('count_info_block', Integer),
    Column('count_block', Integer),
    Column('block_size', Integer),
    # array[][]
    Column('block_array', ARRAY(BigInteger))
)

convolution_table = Table(
    EnumCoderTableName.CONVOLUTION.value,
    StatMetaData().metadata,
    Column('guid', UUID(as_uuid=True), ForeignKey("coder.guid"), primary_key=True),
    Column('count_polynomial', Integer),
    Column('count_input_bits', Integer),
    Column('count_output_bits', Integer),
    Column('count_registers', Integer)
)
