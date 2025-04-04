"""initial migrate

Revision ID: 0c941dbaa46c
Revises: 
Create Date: 2025-04-03 17:17:28.363275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c941dbaa46c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('downloads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('file_url', sa.String(length=300), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gallery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_firstname', sa.String(length=50), nullable=False),
    sa.Column('sender_lastname', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('mobile_number', sa.String(), nullable=True),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ministries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('notice_text', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pastors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ministry_projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ministry_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ministry_id'], ['ministries.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('contact_message_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contact_message_id'], ['messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_images')
    op.drop_table('notifications')
    op.drop_table('ministry_projects')
    op.drop_table('users')
    op.drop_table('projects')
    op.drop_table('pastors')
    op.drop_table('notices')
    op.drop_table('ministries')
    op.drop_table('messages')
    op.drop_table('gallery')
    op.drop_table('downloads')
    # ### end Alembic commands ###
