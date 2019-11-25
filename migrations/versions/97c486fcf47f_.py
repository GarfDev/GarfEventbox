"""empty message

Revision ID: 97c486fcf47f
Revises: 25bfcae7a930
Create Date: 2019-11-25 03:26:23.851556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c486fcf47f'
down_revision = '25bfcae7a930'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('qr_code', sa.String(), nullable=True))
    op.add_column('tickets', sa.Column('number', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets', 'number')
    op.drop_column('order_items', 'qr_code')
    # ### end Alembic commands ###