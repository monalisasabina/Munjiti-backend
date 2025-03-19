"""Recreating ministry_projects with id column

Revision ID: 8f7e92f05f57
Revises: a7d6254212ee
Create Date: 2025-03-19 16:18:52.186228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f7e92f05f57'
down_revision = 'a7d6254212ee'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('ministry_projects')  # Drop old table
    op.create_table(
        'ministry_projects',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ministry_id', sa.Integer(), sa.ForeignKey('ministries.id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
    )

def downgrade():
    op.drop_table('ministry_projects')  # Drop new table
    op.create_table(
        'ministry_projects',
        sa.Column('ministry_id', sa.Integer(), sa.ForeignKey('ministries.id'), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), nullable=False),
    )


    # ### end Alembic commands ###
