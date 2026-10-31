"""Tests for build_report (Part A)."""

from datetime import date
from pathlib import Path

from audit.loader import load_roster, load_users
from audit.report import build_report

DATA = Path(__file__).parent.parent / "sample_data"
AUDIT_DATE = date(2026, 10, 30)


def make_report():
    users = load_users(DATA / "users.csv")
    roster = load_roster(DATA / "hr_roster.csv")
    return build_report(users, roster, AUDIT_DATE)


def test_report_has_all_keys():
    assert set(make_report().keys()) == {
        "audit_date",
        "total_accounts",
        "active_accounts",
        "inactive",
        "no_mfa",
        "orphaned",
        "admins",
        "accounts_with_issues",
    }


def test_report_counts():
    report = make_report()
    assert report["audit_date"] == "2026-10-30"
    assert report["total_accounts"] == 20
    assert report["active_accounts"] == 18


def test_report_reuses_the_checks():
    report = make_report()
    assert report["orphaned"] == [
        "jack.wilson@brightpath.example",
        "olivia.chen@brightpath.example",
    ]
    assert report["admins"]["admin_count"] == 5


def test_people_in_several_lists_are_counted_once():
    # emma, henry, kara, olivia (inactive) + ben, david (no MFA) + jack (left) = 7 people
    assert make_report()["accounts_with_issues"] == 7
