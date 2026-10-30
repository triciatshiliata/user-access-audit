"""Command-line version of the audit.

Usage:
    python -m audit.cli sample_data/users.csv sample_data/hr_roster.csv
"""

import sys
from datetime import date

from audit.checks import (
    check_admin_count,
    find_inactive_accounts,
    find_orphaned_accounts,
    find_users_without_mfa,
)
from audit.loader import load_roster, load_users


def print_section(title, run_check):
    print(f"\n== {title} ==")
    try:
        result = run_check()
    except NotImplementedError:
        print("  (not built yet)")
        return
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"  {key}: {value}")
    elif result:
        for email in result:
            print(f"  - {email}")
    else:
        print("  none found")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    users = load_users(sys.argv[1])
    roster = load_roster(sys.argv[2])
    today = date.today()

    print(f"User Access Audit - {today}  ({len(users)} accounts)")
    print_section("Inactive accounts (90+ days)", lambda: find_inactive_accounts(users, today))
    print_section("Accounts without MFA", lambda: find_users_without_mfa(users))
    print_section("Accounts of people who left", lambda: find_orphaned_accounts(users, roster))
    print_section("Admin accounts", lambda: check_admin_count(users))


if __name__ == "__main__":
    main()
