"""Tests for comment normalization."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from normalize_comments import clean_text, normalize_comment


def _make_item(id: str = "COMMENT-001", **attrs) -> dict:
    base: dict = {
        "title": "Test Comment",
        "firstName": "Jane",
        "lastName": "Doe",
        "organization": "Test Org",
        "postedDate": "2026-03-01",
        "documentType": "Public Submission",
        "docketId": "EAC-2026-0067",
        "comment": "This is a test comment.",
        "withdrawn": False,
        "attachmentCount": 0,
    }
    base.update(attrs)
    return {"id": id, "attributes": base}


# --- clean_text ---

def test_clean_text_strips_whitespace():
    assert clean_text("  hello   world  ") == "hello world"


def test_clean_text_none():
    assert clean_text(None) == ""


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_clean_text_internal_newlines():
    assert clean_text("line1\n  line2") == "line1 line2"


# --- normalize_comment ---

def test_normalize_basic_fields():
    item = _make_item()
    result = normalize_comment(item)
    assert result["id"] == "COMMENT-001"
    assert result["first_name"] == "Jane"
    assert result["last_name"] == "Doe"
    assert result["organization"] == "Test Org"
    assert result["submitted_date"] == "2026-03-01"
    assert result["comment_text"] == "This is a test comment."
    assert result["docket_id"] == "EAC-2026-0067"


def test_normalize_withdrawn_false():
    result = normalize_comment(_make_item(withdrawn=False))
    assert result["withdrawn"] is False


def test_normalize_withdrawn_true():
    result = normalize_comment(_make_item(withdrawn=True))
    assert result["withdrawn"] is True


def test_normalize_no_attachments():
    result = normalize_comment(_make_item(attachmentCount=0))
    assert result["has_attachments"] is False


def test_normalize_has_attachments():
    result = normalize_comment(_make_item(attachmentCount=3))
    assert result["has_attachments"] is True


def test_normalize_missing_attributes():
    item: dict = {"id": "X", "attributes": {}}
    result = normalize_comment(item)
    assert result["id"] == "X"
    assert result["comment_text"] == ""
    assert result["first_name"] == ""
    assert result["organization"] == ""
    assert result["withdrawn"] is False
    assert result["has_attachments"] is False


def test_normalize_falls_back_to_receiveDate():
    item = _make_item()
    del item["attributes"]["postedDate"]
    item["attributes"]["receiveDate"] = "2026-04-01"
    result = normalize_comment(item)
    assert result["submitted_date"] == "2026-04-01"


def test_normalize_cleans_comment_text():
    item = _make_item(comment="  lots   of  spaces  ")
    result = normalize_comment(item)
    assert result["comment_text"] == "lots of spaces"
