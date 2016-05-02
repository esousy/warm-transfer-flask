"""empty message

Revision ID: af406a14a5dd
Revises: None
Create Date: 2016-05-02 14:57:59.321583

"""

# revision identifiers, used by Alembic.
revision = 'af406a14a5dd'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active_calls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.String(), nullable=False),
    sa.Column('conference_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('active_calls')
    ### end Alembic commands ###