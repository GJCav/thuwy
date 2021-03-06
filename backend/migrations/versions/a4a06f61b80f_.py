"""empty message

Revision ID: a4a06f61b80f
Revises: d548cad42827
Create Date: 2022-02-05 17:54:44.737605

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "a4a06f61b80f"
down_revision = "d548cad42827"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("privilege")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "privilege",
        sa.Column(
            "id", mysql.INTEGER(display_width=11), autoincrement=True, nullable=False
        ),
        sa.Column("openid", mysql.VARCHAR(length=64), nullable=True),
        sa.Column(
            "scopeId",
            mysql.INTEGER(display_width=11),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["openid"], ["user.openid"], name="privilege_ibfk_1"),
        sa.ForeignKeyConstraint(
            ["scopeId"], ["oauth_scope.id"], name="privilege_ibfk_2"
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###
