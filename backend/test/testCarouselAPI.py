import pytest
from config4test import R, baseUrl

import sys

sys.path.append("..")
import app.timetools as timestamp
import app.checkargs as CheckArgs

crlUrl = baseUrl + "carousel/"


def assertCarouselMsg(msg: dict, all=False):
    assert CheckArgs.hasAttrs(
        msg, ["id", "owner", "st", "ed", "content"]
    ), f"missing property: {msg}"
    assert CheckArgs.areStr(msg, ["owner", "content"]), f"wrong str type: {msg}"
    assert CheckArgs.areUint64(msg, ["st", "ed"]), f"wrong uint type: {msg}"

    if all:
        assert CheckArgs.hasAttrs(
            msg, ["owner-id", "hide", "last-version"]
        ), f"missing property: {msg}"
        assert CheckArgs.areUint64(msg, ["hide"]), f"wrong uint type: {msg}"
        assert "last-version" in msg
        assert CheckArgs.isStr(msg["owner-id"])


def _addCrl(minSt, minEd, cnt) -> R.Response:
    st = timestamp.clockAfter(timestamp.now(), 0, minSt)
    ed = timestamp.clockAfter(timestamp.now(), 0, minEd)
    reqJson = {"st": st, "ed": ed, "content": cnt}
    res = R.post(crlUrl, json=reqJson)
    return res, st, ed


def _extId(res):
    assert res
    json = res.json()
    assert json["code"] == 0, json
    return json["id"]


testCrlGroup = [[], [], []]  # past  # current  # future


def testAddCarousel():
    testset = [
        # st, ed, content, httpcode, code, group
        (-10, -5, "crl past", 200, 0, 0),
        (-10, 10, "crl curr", 200, 0, 1),
        (5, 10, "crl future", 200, 0, 2),
        (10, 0, "fuck the time", 200, 7, 0),
    ]

    for st, ed, cnt, httpCode, code, gp in testset:
        res, stt, edt = _addCrl(st, ed, cnt)
        assert res.status_code == httpCode
        if httpCode != 200:
            continue
        json = res.json()
        assert json, json
        assert json["code"] == code
        if code != 0:
            continue

        assert "id" in json
        assert CheckArgs.isUint64(json["id"])
        testCrlGroup[gp].append(json["id"])

        id = json["id"]
        res = R.get(f"{crlUrl}{id}/")
        assert res
        json = res.json()
        assert json
        assert json["code"] == 0
        assert "carousel" in json
        msg = json["carousel"]
        assertCarouselMsg(msg, True)
        assert msg["st"] == stt
        assert msg["ed"] == edt
        assert msg["content"] == cnt
        assert msg["hide"] == 0
        assert msg["last-version"] == None


def testGetCurrentCarousel():
    now = timestamp.now()

    res = R.get(crlUrl)
    assert res
    json = res.json()
    assert json, json
    assert json["code"] == 0
    assert "carousels" in json
    crlArr = json["carousels"]
    assert isinstance(crlArr, list)
    for msg in crlArr:
        assertCarouselMsg(msg)
        assert msg["st"] <= now <= msg["ed"]
    allIds = {e["id"] for e in crlArr}
    assert set(testCrlGroup[1]).issubset(allIds)
    assert not allIds.intersection(testCrlGroup[0])
    assert not allIds.intersection(testCrlGroup[2])


def testModifyCarousel():
    res, *_ = _addCrl(10, 20, "modify")
    idBefore = _extId(res)
    st = timestamp.now()
    reqJson = {"hide": 1, "st": st, "content": "modify after"}

    res = R.post(f"{crlUrl}{idBefore}/", json=reqJson)
    assert res
    json = res.json()
    assert json
    assert json["code"] == 0
    assert "id" in json
    idAfter = json["id"]

    assert idBefore != idAfter

    res = R.get(f"{crlUrl}{idAfter}/")
    assert res
    json = res.json()
    assert json["code"] == 0
    assertCarouselMsg(json["carousel"])
    newCrl = json["carousel"]
    assert newCrl["hide"] == 1
    assert newCrl["last-version"] == idBefore
    assert newCrl["st"] == st

    reqJson = {"hide": 0}
    res = R.post(f"{crlUrl}{idAfter}/", json=reqJson)
    assert res
    json = res.json()
    assert json
    assert json["code"] == 0
    assert "id" in json
    idAfterAfter = json["id"]

    assert idAfterAfter != idAfter

    res = R.get(f"{crlUrl}{idAfterAfter}/")
    assert res
    json = res.json()
    assert json["code"] == 0
    assertCarouselMsg(json["carousel"])
    newCrl = json["carousel"]
    assert newCrl["hide"] == 0
    assert newCrl["last-version"] == idAfter
    assert newCrl["st"] == st
