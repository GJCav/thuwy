import json
from urllib import response
from config4test import R, UseAccount, baseUrl

import sys

sys.path.append("..")
from app.comerrs import *
from app.issue.errcode import *

import pytest


test_issue_url = baseUrl + "issue"

SAMPLE_TAGS = ["SampleTag0", "SampleTag1", "SampleTag2"]
SAMPLE_ISSUE = {
    "title": "Sample Title",
    "visibility": "public",
    "tags": ";".join(SAMPLE_TAGS) + ";",
    "content": {"text": "Sample text."},
}


def test_search_overview():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        payload["visibility"] = "public"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id_public = json["issue_id"]

        payload["visibility"] = "protected"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id_protected = json["issue_id"]

        payload["visibility"] = "private"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id_private = json["issue_id"]

        response = R.get(url=f"{test_issue_url}/")
        json = response.json()
        ids = [issue["id"] for issue in json["issues"]]
        assert id_public in ids
        assert id_protected in ids
        assert id_private in ids


def test_search_overview_by_authors():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id = json["issue_id"]
        response = R.get(url=f"{test_issue_url}/", params={"authors": "normal_user"})
        json = response.json()
        print(json)
        ids = [issue["id"] for issue in json["issues"]]
        assert id in ids


def test_search_overview_by_tags():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        payload["tags"] = "A0;A1;"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id01 = json["issue_id"]

        payload["reply_to"] = id01
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id_reply = json["issue_id"]

        del payload["reply_to"]
        payload["tags"] = "A1;A2;"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id12 = json["issue_id"]

        payload["tags"] = "A2;A3;"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id23 = json["issue_id"]

        response = R.get(url=f"{test_issue_url}/", params={"tags": "A0 A1; A1 A2;"})
        json = response.json()
        ids = [issue["id"] for issue in json["issues"]]
        assert id01 in ids
        assert id_reply not in ids
        assert id12 in ids
        assert id23 not in ids


def test_normal_user_post_valid_issue():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        assert json["code"] == 0
        id = json["issue_id"]
        response = R.get(url=f"{test_issue_url}/{id}/")
        json = response.json()
        assert json["code"] == CODE_SUCCESS["code"]
        root_issue = json["issues"][0]
        assert root_issue["title"] == SAMPLE_ISSUE["title"]
        assert root_issue["visibility"] == "protected"
        assert root_issue["tags"] == SAMPLE_TAGS
        assert root_issue["content"] == SAMPLE_ISSUE["content"]


def test_normal_user_post_long_issue():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        payload["title"] = "a" * 1024
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        assert json == CODE_ARG_INVALID


def test_normal_user_query_nonexistent_detail():
    with UseAccount("normal_user"):
        response = R.get(url=f"{test_issue_url}/7777777/")
        json = response.json()
        assert json == CODE_ISSUE_NOT_FOUND


def test_issue_tree_link():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        root_id = json["issue_id"]
        payload["reply_to"] = json["issue_id"]
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        child_id = json["issue_id"]
        response = R.get(url=f"{test_issue_url}/{child_id}/")
        json = response.json()
        assert json["code"] == CODE_SUCCESS["code"]
        assert json["issues"][0]["id"] == root_id
        assert json["issues"][1]["id"] == child_id


def test_edit_issue():
    id = None
    with UseAccount("super_admin"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id = json["issue_id"]

    with UseAccount("normal_user"):
        payload = {"visibility": "public"}
        response = R.post(url=f"{test_issue_url}/{id}/", json=payload)
        json = response.json()
        assert json == CODE_ACCESS_DENIED

    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id = json["issue_id"]

    with UseAccount("super_admin"):
        payload = {"visibility": "public"}
        response = R.post(url=f"{test_issue_url}/{id}/", json=payload)
        json = response.json()
        assert json == CODE_SUCCESS

        response = R.get(url=f"{test_issue_url}/{id}/")
        json = response.json()
        assert json["issues"][0]["visibility"] == "public"


def test_delete_issue():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        id = json["issue_id"]
        response = R.delete(url=f"{test_issue_url}/{id}/")
        json = response.json()
        assert json == CODE_SUCCESS
        response = R.get(url=f"{test_issue_url}/{id}/")
        json = response.json()
        assert json == CODE_ISSUE_NOT_FOUND


def test_query_all_tags():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        response = R.get(url=f"{test_issue_url}/tag/")
        json = response.json()
        assert json["code"] == CODE_SUCCESS["code"]
        for tag in SAMPLE_TAGS:
            assert tag in json["tags"]


def test_query_tags():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        response = R.get(url=f"{test_issue_url}/tag/", params={"keyword": "sample"})
        json = response.json()
        assert json["code"] == CODE_SUCCESS["code"]
        for tag in SAMPLE_TAGS:
            assert tag in json["tags"]


def test_query_tag_detail():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        tag_name = "SampleTag0"
        payload["tags"] = f"{tag_name}s"
        response = R.post(url=f"{test_issue_url}/", json=payload)
        response = R.get(url=f"{test_issue_url}/tag/{tag_name}/")
        json = response.json()
        assert json["code"] == CODE_SUCCESS["code"]
        tag_meta = json["tag_meta"]
        assert tag_meta["name"] == tag_name
