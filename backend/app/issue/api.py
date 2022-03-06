from . import issueRouter
from .errcode import *
from .model import db, IssueTagMeta, Issue
from .types import Visibility
from .utils import _am_admin, _split, _try_modify_visibility

from app.auth import requireScope
from app.comerrs import *

from flask import request
from flask import g
import sqlalchemy

from typing import Any, Dict, List


SAMPLE_ISSUE = {
    "id": 123456,
    "title": "Title",
    "author": "000000",
    "date": 123456789,
    "last_modified_at": 987654321,
    "status": "open",
    "visibility": "public",
    "tags": ["TagA", "TagB"],
    "reply_to": None,
    "root_id": None,
    "content": {},
}


def _get_or_insert_tags(tag_list: List[str]):
    tag_meta_list = []
    for tag in tag_list:
        if tag == "#top":
            if _am_admin():
                pass
            else:
                continue
        tag_meta = db.session.get(IssueTagMeta, {"name": tag})
        if not tag_meta:
            tag_meta = IssueTagMeta()
            tag_meta.name = tag
            db.session.add(tag_meta)
        elif not tag_meta.valid:
            tag_meta.delete = False
        tag_meta_list.append(tag_meta)
    db.session.commit()
    return tag_meta_list


@issueRouter.route("/issue/", methods=["GET"])
@requireScope(["profile"])
def issueSearchOverview():
    """Filter issues with given parameters."""
    page_size = request.args.get(key="page_size", default=10, type=int)
    if (not page_size) or (page_size > 10):
        return CODE_ARG_INVALID
    page_num = request.args.get(key="page_num", default=1, type=int)
    page_num -= 1
    if page_num < 0:
        return CODE_ARG_INVALID
    criteria = sqlalchemy.true()
    # reply_to = request.args.get(key="reply_to", default=None, type=int)
    # if reply_to:
    #     criteria &= Issue.reply_to == reply_to
    root_id = request.args.get(key="root_id", default=None, type=int)
    if root_id:
        criteria &= (Issue.root_id == root_id) | (Issue.id == root_id)
    authors = request.args.get(key="authors", default=g.openid, type=str)
    authors_grouped = _split(authors, ";")
    if authors_grouped:
        author_or_criteria = sqlalchemy.false()
        for author_group in authors_grouped:
            author_and_criteria = sqlalchemy.true()
            author_list = _split(author_group, " ")
            for author in author_list:
                author_and_criteria &= Issue.author == author
            author_or_criteria |= author_and_criteria
        criteria &= author_or_criteria
    visibility = request.args.get(key="visibility", default="all", type=str)
    if visibility == "all":
        pass
    else:
        try:
            visibility = Visibility(visibility)
            criteria &= Issue.visibility == visibility
        except:
            return CODE_ARG_INVALID
    tags = request.args.get(key="tags", default="", type=str)
    tags_grouped = _split(tags, ";")
    if tags_grouped:
        tag_or_criteria = sqlalchemy.false()
        for tag_group in tags_grouped:
            tag_and_criteria = sqlalchemy.true()
            tag_list = _split(tag_group, " ")
            for tag in tag_list:
                tag_and_criteria &= Issue.tags.any(IssueTagMeta.name == tag)
            tag_or_criteria |= tag_and_criteria
        criteria &= tag_or_criteria
    start_time = request.args.get(key="start_time", default=None, type=int)
    if start_time:
        criteria &= Issue.last_modified_at >= start_time
    end_time = request.args.get(key="end_time", default=None, type=int)
    if end_time:
        criteria &= Issue.last_modified_at < end_time
    issues = (
        db.session.query(Issue)
        .filter(criteria)
        .filter(Issue.root_criteria())
        .filter(Issue.visible_criteria())
    )
    sort_by = request.args.get(key="sort_by", default="last_modified_at", type=str)
    sort_by = _split(sort_by, ";")
    try:
        for by in sort_by:
            issues = issues.order_by(sqlalchemy.desc(eval(f"Issue.{by}")))
    except:
        return CODE_ARG_INVALID
    response = CODE_SUCCESS.copy()
    response["count"] = issues.count()
    issues: List[Dict[str, Any]] = [issue.overview for issue in issues.all()]
    issues.sort(key=lambda issue: "#top" in issue["tags"], reverse=True)
    issues = issues[
        min(len(issues), page_num * page_size) : min(
            len(issues), (page_num + 1) * page_size
        )
    ]
    response["issues"] = issues
    return response


@issueRouter.route("/issue/<int:id>/", methods=["GET"])
@requireScope(["profile"])
def issueQueryDetail(id: int):
    """Search for all issues related with the specific issue."""
    current_issue: Issue = db.session.get(Issue, {"id": id})
    if not (current_issue and current_issue.visible):
        return CODE_ISSUE_NOT_FOUND
    root_id = current_issue.id if current_issue.is_root else current_issue.root_id
    issues: list[Issue] = (
        db.session.query(Issue)
        .filter_by(root_id=root_id)
        .filter(Issue.visible_criteria())
        .order_by(sqlalchemy.asc(Issue.date), sqlalchemy.asc(Issue.id))
        .all()
    )
    root_issue: Issue = db.session.get(Issue, {"id": root_id})
    if root_issue and root_issue.visible:
        issues.insert(0, root_issue)
    response = CODE_SUCCESS.copy()
    issues: List[Dict[str, Any]] = [issue.detail for issue in issues]
    issues.sort(key=lambda issue: "#top" in issue["tags"], reverse=True)
    response["issues"] = issues
    return response


@issueRouter.route("/issue/", methods=["POST"])
@requireScope(["profile"])
def issueNew():
    """Post a new issue."""
    # extract args
    payload: dict[str, Any] = request.get_json()
    title: str = payload.get("title", "")
    visibility: str = payload.get("visibility", Visibility.PUBLIC)
    tags: str = payload.get("tags", "")
    tag_list: List[str] = _split(tags, ";")
    reply_to: int = payload.get("reply_to", None)
    # check args
    try:
        visibility = _try_modify_visibility(visibility)
    except:
        return CODE_ARG_INVALID
    # make changes
    new_issue = Issue()
    new_issue.title = title
    new_issue.author = g.openid
    new_issue.visibility = visibility
    new_issue.content = payload.get("content", {})
    # TODO @liblaf attachments
    new_issue.tags = _get_or_insert_tags(tag_list)
    try:
        db.session.add(new_issue)
        db.session.commit()
    except:
        return CODE_ARG_INVALID
    new_issue.reply_to = reply_to
    if reply_to:
        parent: Issue = db.session.get(Issue, {"id": reply_to})
        if parent and parent.visible:
            new_issue.root_id = parent.id if parent.is_root else parent.root_id
        else:
            return CODE_ISSUE_NOT_FOUND
    db.session.commit()
    response = CODE_SUCCESS.copy()
    response["issue_id"] = new_issue.id
    return response


@issueRouter.route("/issue/<int:id>/", methods=["POST"])
@requireScope(["profile"])
def issueEdit(id: int):
    """Edit an existing issue."""
    # find target issue
    issue: Issue = db.session.get(Issue, {"id": id})
    if not (issue and issue.visible):
        return CODE_ISSUE_NOT_FOUND
    if not issue.editable:
        return CODE_ACCESS_DENIED
    # extract args
    payload: dict[str, Any] = request.get_json()
    title: str = payload.get("title", None)
    visibility: str = payload.get("visibility", None)
    tags: str = payload.get("tags", None)
    content: dict = payload.get("content", None)
    # check args
    if visibility:
        try:
            visibility = _try_modify_visibility(visibility)
        except:
            return CODE_ARG_INVALID
    # update issue
    issue.title = title or issue.title
    issue.visibility = visibility or issue.visibility
    if tags:
        tag_list: List[str] = _split(tags)
        issue.tags = _get_or_insert_tags(_split(tag_list))
    issue.content = content or issue.content
    db.session.commit()
    response = CODE_SUCCESS
    return response


@issueRouter.route("/issue/<int:id>/", methods=["DELETE"])
@requireScope(["profile"])
def issueDelete(id: int):
    """Delete an issue."""
    # find target issue
    issue: Issue = db.session.query(Issue).get({"id": id})
    if not (issue and issue.visible):
        return CODE_ISSUE_NOT_FOUND
    if not issue.editable:
        return CODE_ACCESS_DENIED
    issue.delete = True
    db.session.commit()
    return CODE_SUCCESS


@issueRouter.route("/issue/tag/", methods=["GET"])
@requireScope(["profile"])
def issueTagSearchOverview():
    """Search for all tags which contain specific keywords"""
    tags = request.args.get("tags", "")
    result = (
        db.session.query(IssueTagMeta)
        .filter(IssueTagMeta.name.ilike(f"%{'%'.join(tags.split())}%"))
        .filter(IssueTagMeta.valid_criteria())
    )
    response = CODE_SUCCESS.copy()
    response["tags"] = [tag_meta.name for tag_meta in result.all()]
    return response


@issueRouter.route("/issue/tag/<name>/", methods=["GET"])
@requireScope(["profile"])
def issueTagSearchDetail(name: str):
    """Search for detailed information of the tag"""
    tag_meta: IssueTagMeta = db.session.get(IssueTagMeta, {"name": name})
    if tag_meta and (tag_meta.valid):
        response = CODE_SUCCESS.copy()
        response["tag_meta"] = tag_meta.detail
        return response
    else:
        return CODE_TAG_NOT_FOUND


@issueRouter.route("/issue/tag/<name>/", methods=["DELETE"])
@requireScope(["profile dayi"])
def issueTagDelete(name: str):
    """Delete tag named `name`."""
    tag_meta: IssueTagMeta = db.session.get(IssueTagMeta, {"name": name})
    if tag_meta and (tag_meta.valid):
        tag_meta.delete = True
        db.session.commit()
        return CODE_SUCCESS
    else:
        return CODE_TAG_NOT_FOUND
