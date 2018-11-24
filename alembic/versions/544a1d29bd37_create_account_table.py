"""create account table

Revision ID: 544a1d29bd37
Revises: 
Create Date: 2018-11-21 18:17:46.362471

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import Integer, Float, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

revision = '544a1d29bd37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'coder',
        sa.Column('guid', UUID, primary_key=True),
        sa.Column('coder_type', Integer),
        sa.Column('coder_speed', Float),
        sa.Column('input_length', Integer),
        sa.Column('additional_length', Integer),
        sa.Column('interleaver', Boolean),
        sa.Column('description', String(200))
    )


def downgrade():
    op.drop_table('account')
