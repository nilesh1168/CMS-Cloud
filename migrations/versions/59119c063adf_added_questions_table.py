"""added questions table

Revision ID: 59119c063adf
Revises: b0e20ea9eb9b
Create Date: 2020-05-21 18:25:30.428706

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '59119c063adf'
down_revision = 'b0e20ea9eb9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Student_Stud')
    op.add_column('Question_Table', sa.Column('session_id', sa.Integer(), nullable=True))
    op.alter_column('Question_Table', 'question',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=750),
               existing_nullable=True)
    op.create_foreign_key(None, 'Question_Table', 'Session', ['session_id'], ['s_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Question_Table', type_='foreignkey')
    op.alter_column('Question_Table', 'question',
               existing_type=sa.String(length=750),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
    op.drop_column('Question_Table', 'session_id')
    op.create_table('Student_Stud',
    sa.Column('session_id', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('stud_id', mysql.BIGINT(), autoincrement=False, nullable=True),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###