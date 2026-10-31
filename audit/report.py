"""Combine the four checks into one report (used by the web app)."""

from audit.checks import (
    active_only,
    check_admin_count,
    find_inactive_accounts,
    find_orphaned_accounts,
    find_users_without_mfa,
)


# ---------------------------------------------------------------------------
# YOUR TURN (Part A)
# ---------------------------------------------------------------------------
def build_report(users, roster, audit_date):
    """Run every check and return ONE dictionary with all the results.

    Return a dict with exactly these keys:
        {
            "audit_date": "2026-10-30",      # audit_date as text: audit_date.isoformat()
            "total_accounts": 20,             # every row in users
            "active_accounts": 18,            # only status == "Active"
            "inactive": [...],                # result of find_inactive_accounts
            "no_mfa": [...],                  # result of find_users_without_mfa
            "orphaned": [...],                # result of find_orphaned_accounts
            "admins": {...},                  # result of check_admin_count
            "accounts_with_issues": 7,        # how many DIFFERENT emails appear in
                                              # inactive, no_mfa or orphaned
        }

    Hints:
    - You already wrote every check - just call them and store the results.
    - Someone can be in two lists (olivia is in all three!) but should only
      be counted once. A Python set removes duplicates:
          set(["a", "b", "a"])  ->  {"a", "b"}
      and you can join lists with +  :  list1 + list2
    """
    raise NotImplementedError
