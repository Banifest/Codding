# coding=utf-8
from sqlalchemy import Table, Column, Integer, Sequence, MetaData

Table(
    'case_result',
    MetaData(),
    Column('id', Integer, Sequence('some_id_seq'), primary_key=True)
)