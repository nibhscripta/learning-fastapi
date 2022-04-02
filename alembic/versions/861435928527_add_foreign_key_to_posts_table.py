"""add foreign key to posts table

Revision ID: 861435928527
Revises: b507a38d349c
Create Date: 2022-04-02 17:50:00.491181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '861435928527'
down_revision = 'b507a38d349c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
