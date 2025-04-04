"""empty message

Revision ID: 0b06d31da999
Revises: 679b9006abfa
Create Date: 2025-04-03 17:45:06.431625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b06d31da999'
down_revision = '679b9006abfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.alter_column('contact_message_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('notifications_contact_message_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'messages', ['contact_message_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('notifications_contact_message_id_fkey', 'messages', ['contact_message_id'], ['id'])
        batch_op.alter_column('contact_message_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
