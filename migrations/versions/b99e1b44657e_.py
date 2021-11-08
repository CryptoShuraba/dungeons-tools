"""empty message

Revision ID: b99e1b44657e
Revises: 1a7a98cdbd09
Create Date: 2021-11-08 17:08:16.497616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b99e1b44657e'
down_revision = '1a7a98cdbd09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'dungeons_monster_coppers', 'monster_list', ['monster_tokenid'], ['token_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'dungeons_monster_coppers', type_='foreignkey')
    # ### end Alembic commands ###
