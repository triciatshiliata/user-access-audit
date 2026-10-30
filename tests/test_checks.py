"""Tests for the four checks, run against the sample data.

Run them with:   pytest
A check you haven't written yet shows up as FAILED - that's expected.
"""

from datetime import date
from pathlib import Path

import pytest

from audit.checks import (
    check_admin_count,
    find_inactive_accounts,
    find_orphaned_accounts,
    find_users_without_mfa,
)
from audit.loader import load_roster, load_users

DATA = Path(__file__).parent.parent / "sample_data"
AUDIT_DATE = date(2026, 10, 30)


@pytest.fixture
def users():
    return load_users(DATA / "users.csv")


@pytest.fixture
def roster():
    return load_roster(DATA / "hr_roster.csv")


def test_inactive_accounts(users):
    assert find_inactive_accounts(users, AUDIT_DATE) == [
        "emma.brooks@brightpath.example",   # last login in May
        "henry.patel@brightpath.example",   # never logged in
        "kara.james@brightpath.example",    # last login in June
        "olivia.chen@brightpath.example",   # last login in July
    ]


def test_exactly_90_days_is_not_inactive(users):
    # maya.singh last logged in on Aug 1 = exactly 90 days before the audit
    assert "maya.singh@brightpath.example" not in find_inactive_accounts(users, AUDIT_DATE)


def test_suspended_accounts_are_ignored(users):
    # isabel.moreno is suspended and hasn't logged in since March
    assert "isabel.moreno@brightpath.example" not in find_inactive_accounts(users, AUDIT_DATE)


def test_users_without_mfa(users):
    assert find_users_without_mfa(users) == [
        "ben.carter@brightpath.example",
        "david.kim@brightpath.example",
        "henry.patel@brightpath.example",
        "kara.james@brightpath.example",
        "olivia.chen@brightpath.example",
    ]


def test_orphaned_accounts(users, roster):
    # jack.wilson and olivia.chen left the company; tina.ward also left but is suspended
    assert find_orphaned_accounts(users, roster) == [
        "jack.wilson@brightpath.example",
        "olivia.chen@brightpath.example",
    ]


def test_roster_email_case_does_not_matter(users, roster):
    # The roster spells it "Grace.Lee@BrightPath.example" - she still works here
    assert "grace.lee@brightpath.example" not in find_orphaned_accounts(users, roster)


def test_admin_count(users):
    result = check_admin_count(users)
    assert result["admin_count"] == 5
    assert result["active_count"] == 18
    assert result["ratio"] == 0.28
    assert result["too_many"] is True
    assert result["admins"] == [
        "alice.nguyen@brightpath.example",
        "ben.carter@brightpath.example",
        "frank.osei@brightpath.example",
        "kara.james@brightpath.example",
        "rosa.lopez@brightpath.example",
    ]


def test_admin_count_with_higher_limit(users):
    assert check_admin_count(users, max_ratio=0.30)["too_many"] is False
