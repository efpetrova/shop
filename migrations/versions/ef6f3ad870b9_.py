"""empty message

Revision ID: ef6f3ad870b9
Revises: 53900d8e18c7
Create Date: 2020-11-05 15:48:24.313268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef6f3ad870b9'
down_revision = '53900d8e18c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_now', sa.DateTime(), nullable=True))
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('date_now')

    # ### end Alembic commands ###
