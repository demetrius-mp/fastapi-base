"""add Invoice.created_at field

Revision ID: 77e3a8c67488
Revises: 2884043fb162
Create Date: 2022-04-19 19:08:21.408309

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "77e3a8c67488"
down_revision = "2884043fb162"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("invoice", sa.Column("created_at", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("invoice", "created_at")
    # ### end Alembic commands ###
