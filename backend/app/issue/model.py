from app.models import db
from app.models import WECHAT_OPENID, SNOWFLAKE_ID


# Common parameters when construct a new `Column` object:
#     name, type_, default, doc, nullable, primary_key, unique
IssueTitleTy = db.VARCHAR(80)
IssueTagNameTy = db.VARCHAR(80)
issue_tag = db.Table(
    "issue_tag",
    db.Column("issue_id", SNOWFLAKE_ID, db.ForeignKey("issue.id"), primary_key=True),
    db.Column(
        "tag_name",
        IssueTagNameTy,
        db.ForeignKey("issue_tag_meta.name"),
        primary_key=True,
    ),
)


class IssueTagMeta(db.Model):
    __tablename__ = "issue_tag_meta"
    name = db.Column("name", IssueTagNameTy, primary_key=True, unique=True)
    delete = db.Column(
        "delete",
        db.BOOLEAN,
        doc='`True` if the tag has been moved to "Trash"',
        nullable=False,
        default=False,
    )
    description = db.Column("description", db.TEXT, default="")


class Issue(db.Model):
    __tablename__ = "issue"
    id = db.Column("id", SNOWFLAKE_ID, primary_key=True, unique=True)
    delete = db.Column(
        "delete",
        db.BOOLEAN,
        doc='`True` if the tag has been moved to "Trash"',
        nullable=False,
        default=False,
    )
    title = db.Column("title", IssueTitleTy, default="")
    author = db.Column("author", WECHAT_OPENID)
    date = db.Column("date", db.BIGINT, doc="creation time stored in `timestamp` form")
    last_modified_at = db.Column(
        "last_modified_at",
        db.BIGINT,
        doc="date modified sotred in `timestamp` form",
    )
    reply_to = db.Column("reply_to", SNOWFLAKE_ID, doc="ID of the Issue replying to")
    root_id = db.Column(
        "root_id",
        SNOWFLAKE_ID,
        doc="ID of the root Issue, equals to `self.id` if `self` is an root Issue",
    )
    tags = db.relationship(
        "tags",
        secondary=issue_tag,
        lazy="subquery",
        backref=db.backref("issues", lazy=True),
    )
    content = db.Column("content", db.JSON)
    # attachments = db.Column("attachments")
    # likes = db.Column("likes")
    # favorites = db.Column("favorites")
