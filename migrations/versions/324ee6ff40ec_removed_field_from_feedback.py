"""removed field from Feedback

Revision ID: 324ee6ff40ec
Revises: 953cf3888fc3
Create Date: 2020-04-02 16:32:45.182192

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '324ee6ff40ec'
down_revision = '953cf3888fc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Session', 'time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Session', sa.Column('time', mysql.TIME(), nullable=False))
    # ### end Alembic commands ###
