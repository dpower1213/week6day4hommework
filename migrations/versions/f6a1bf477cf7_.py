"""empty message

Revision ID: f6a1bf477cf7
Revises: 3b872dc7d648
Create Date: 2022-02-11 11:50:49.682985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6a1bf477cf7'
down_revision = '3b872dc7d648'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pokemon', sa.Column('front_shiny', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pokemon', 'front_shiny')
    # ### end Alembic commands ###
