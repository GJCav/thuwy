from . import issueRouter
from app.comerrs import *
from app.auth import requireScope

from flask import request

SAMPLE_ISSUE = {
    "id": 123456,
    "title": "Title",
    "author": "000000",
    "date": 123456789,
    "last_modified_at": 987654321,
    "status": "open",
    "visibility": "public",
    "tags": ["教务", "答疑"],
    "reply_to": None,
    "root_id": None,
    "content": {},
}


@issueRouter.route("/issue/", methods=["GET"])
@requireScope(["profile"])
def issueSearchOverview():
    """Filter issues with given parameters."""
    # get & check args
    page_size = request.args.get(key="page_size", default=10, type=int)
    page_size = 10 if page_size > 10 else page_size
    page_num = request.args.get(key="page_num", default=1, type=int)
    page_num -= 1
    sort_by = request.args.get(key="sort_by", default="last_modified_at", type=str)
    reply_to = request.args.get(key="reply_to", default=None, type=int)
    root_id = request.args.get(key="root_id", default=None, type=int)
    authors = request.args.get(key="authors", default="", type=str)
    tags = request.args.get(key="tags", default="", type=str)
    visibility = request.args.get(key="visibility", default="", type=str)
    start_time = request.args.get(key="start_time", default=0, type=int)
    end_time = request.args.get(key="end_time", default=None, type=int)
    response = {"count": 0, "issues": [SAMPLE_ISSUE]}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/<int:id>/", methods=["GET"])
@requireScope(["profile"])
def issueSearchDetail(id: int):
    """Search for all issues related with the specific issue."""
    response = {"issues": [SAMPLE_ISSUE]}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/", methods=["POST"])
@requireScope(["profile"])
def issueNew():
    """Post a new issue."""
    response = {"issue_id": 1}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/<int:id>/", methods=["POST"])
@requireScope(["profile"])
def issueEdit(id: int):
    """Edit an existing issue."""
    response = {}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/<int:id>/", methods=["DELETE"])
@requireScope(["profile"])
def issueDelete(id: int):
    """Delete an issue."""
    response = {}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/tag/", methods=["GET"])
@requireScope(["profile"])
def issueTagSearchOverview():
    """Search for all tags which contain specific keywords"""
    response = {"tags": ["教务", "答疑"]}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/tag/<name>/", methods=["GET"])
@requireScope(["profile"])
def issueTagSearchDetail(name: str):
    """Search for detailed information of the tag"""
    response = {"tag_meta": {"name": name, "description": ""}}
    response.update(CODE_SUCCESS)
    return response


@issueRouter.route("/issue/tag/<name>/", methods=["DELETE"])
@requireScope(["profile admin", "profile dayi"])
def issueTagDelete(name: str):
    """Delete tag named `name`."""
    response = {}
    response.update(CODE_SUCCESS)
    return response
