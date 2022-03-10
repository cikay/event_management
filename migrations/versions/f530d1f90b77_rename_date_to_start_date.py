"""Rename date to start_date

Revision ID: f530d1f90b77
Revises: 84f8c3445d16
Create Date: 2022-03-10 20:45:25.058709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f530d1f90b77'
down_revision = '84f8c3445d16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('start_date', sa.DateTime(), nullable=False))
    op.drop_column('event', 'date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('event', 'start_date')
    # ### end Alembic commands ###