"""empty message

Revision ID: 6f8c009bc96f
Revises: 25fde8af8870
Create Date: 2018-04-17 20:44:17.020023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f8c009bc96f'
down_revision = '25fde8af8870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('location', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'location')
    # ### end Alembic commands ###
