from config4test import R, UseAccount, baseUrl

import sys

sys.path.append("..")
from app.comerrs import *
from app.item.errcode import *
import app.checkargs as CheckArgs

import pytest


test_issue_url = baseUrl + "issue"

SAMPLE_ISSUE = {
    "title": "Sample Title",
    "visibility": "public",
    "tags": "SampleTag0;SampleTag1;SampleTag2;",
    "content": {"text": "Sample text."},
}


def test_normal_user_post_valid_issue():
    with UseAccount("normal_user"):
        payload = SAMPLE_ISSUE.copy()
        response = R.post(url=f"{test_issue_url}/", json=payload)
        json = response.json()
        assert json["code"] == 0
        id = json["issue_id"]
        response = R.get(url=f"{test_issue_url}/{id}/")
        json = response.json()
        root_issue = json["issues"][0]
        assert root_issue["title"] == SAMPLE_ISSUE["title"]
        assert root_issue["visibility"] == "protected"
        assert root_issue["tags"] == ["SampleTag0", "SampleTag1", "SampleTag2"]
        assert root_issue["content"] == SAMPLE_ISSUE["content"]
