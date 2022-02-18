from .types import Visibility
from .utils import _am_admin

from app.models import db
from app.models import WECHAT_OPENID
from app import timetools

from flask import g
import sqlalchemy

from typing import Any


# Common parameters when construct a new `Column` object:
#     name, type_, default, doc, nullable, primary_key, unique


IssueTitleTy = db.VARCHAR(80)
IssueTagNameTy = db.VARCHAR(80)


issue_tag = db.Table(
    "issue_tag",
    db.Column("issue_id", db.Integer, db.ForeignKey("issue.id"), primary_key=True),
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

    @property
    def valid(self) -> bool:
        return not self.delete

    @staticmethod
    def valid_criteria(validity: bool = True):
        return IssueTagMeta.delete == (not validity)

    @property
    def detail(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description}


class Issue(db.Model):
    __tablename__ = "issue"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True, unique=True)
    delete = db.Column(
        "delete",
        db.BOOLEAN,
        doc='`True` if the tag has been moved to "Trash"',
        nullable=False,
        default=False,
    )
    title = db.Column("title", IssueTitleTy, default="")
    author = db.Column("author", WECHAT_OPENID)
    date = db.Column(
        "date",
        db.BIGINT,
        default=lambda: timetools.now(),
        doc="creation time stored in `timestamp` form",
    )
    last_modified_at = db.Column(
        "last_modified_at",
        db.BIGINT,
        doc="date modified sotred in `timestamp` form",
        onupdate=lambda: timetools.now(),
    )
    reply_to = db.Column("reply_to", db.Integer, doc="ID of the Issue replying to")
    root_id = db.Column(
        "root_id",
        db.Integer,
        doc="ID of the root Issue, equals to `self.id` if `self` is an root Issue",
    )
    tags = db.relationship(
        "IssueTagMeta",
        secondary=issue_tag,
        lazy="subquery",
        backref=db.backref("issues", lazy=True),
    )
    visibility = db.Column("visibility", db.Enum(Visibility))
    content = db.Column("content", db.JSON)
    # attachments = db.Column("attachments")
    # likes = db.Column("likes")
    # favorites = db.Column("favorites")

    @property
    def valid(self) -> bool:
        return not self.delete

    def __bool__(self) -> bool:
        return self.valid

    @staticmethod
    def valid_criteria(validity: bool = True):
        return Issue.delete == (not validity)

    @property
    def written_by(self, author: str = None) -> bool:
        author = author or g.openid
        return self.valid and (self.author == author)

    @staticmethod
    def author_criteria(author: str = None):
        author = author or g.openid
        return Issue.valid_criteria() & (Issue.author == author)

    @property
    def visible(self) -> bool:
        return self.valid and (
            _am_admin() or self.written_by or self.visibility == Visibility.PUBLIC
        )

    @staticmethod
    def visible_criteria():
        return Issue.editable_criteria() | (
            Issue.valid_criteria() & (Issue.visibility == Visibility.PUBLIC)
        )

    @property
    def editable(self) -> bool:
        return self.visible and (_am_admin() or self.written_by)

    @staticmethod
    def editable_criteria():
        return Issue.valid_criteria() & (
            sqlalchemy.true() if _am_admin() else Issue.author_criteria()
        )

    @property
    def is_root(self) -> bool:
        return not self.reply_to

    @staticmethod
    def root_criteria():
        return Issue.reply_to.is_(None)

    @staticmethod
    def not_root_criteria():
        return Issue.reply_to.is_not(None)

    @property
    def overview(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "date": self.date,
            "last_modified_at": self.last_modified_at,
            "visibility": self.visibility.value,
            "tags": [tag_meta.name for tag_meta in self.tags],
            "reply_to": self.reply_to,
            "root_id": self.root_id,
        }

    @property
    def detail(self) -> dict[str, Any]:
        return self.overview.update({"content": self.content})
