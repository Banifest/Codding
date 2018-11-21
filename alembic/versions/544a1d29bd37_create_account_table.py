"""create account table

Revision ID: 544a1d29bd37
Revises: 
Create Date: 2018-11-21 18:17:46.362471

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '544a1d29bd37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('account')
