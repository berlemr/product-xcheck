"""added inventory

Revision ID: 1ec5accac571
Revises: 5db04ef84bc9
Create Date: 2019-12-19 20:13:43.887669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ec5accac571'
down_revision = '5db04ef84bc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=200), nullable=True),
    sa.Column('item', sa.String(length=200), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inventory')
    # ### end Alembic commands ###