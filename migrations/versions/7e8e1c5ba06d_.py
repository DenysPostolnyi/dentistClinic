"""empty message

Revision ID: 7e8e1c5ba06d
Revises: 67b2ea5ac58b
Create Date: 2023-02-27 10:10:59.872913

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7e8e1c5ba06d'
down_revision = '67b2ea5ac58b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Doctors', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=10),
               existing_nullable=True)

    with op.batch_alter_table('Patients', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Patients', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('Doctors', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
