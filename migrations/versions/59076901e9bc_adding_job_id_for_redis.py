"""Adding job id for redis.

Revision ID: 59076901e9bc
Revises: 0c61bd60e0aa
Create Date: 2023-03-15 03:24:36.662887

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "59076901e9bc"
down_revision = "0c61bd60e0aa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("itinerary", schema=None) as batch_op:
        batch_op.add_column(sa.Column("job_id", sa.String(length=64), nullable=True))
        batch_op.alter_column("markdown", existing_type=sa.TEXT(), nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("itinerary", schema=None) as batch_op:
        batch_op.alter_column("markdown", existing_type=sa.TEXT(), nullable=False)
        batch_op.drop_column("job_id")

    # ### end Alembic commands ###
