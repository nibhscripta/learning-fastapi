"""add content column to posts table

Revision ID: 6b167e4218f3
Revises: ff61d6dcf15d
Create Date: 2022-04-02 17:40:52.779920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b167e4218f3'
down_revision = 'ff61d6dcf15d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
