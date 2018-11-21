# coding=utf-8
from sqlalchemy import Table, Column, Integer, Sequence

Table(
    'case_result',
    metadata,
    Column('id', Integer, Sequence('some_id_seq'), primary_key=True)
)