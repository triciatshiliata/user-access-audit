"""The four security checks.

Every check only looks at ACTIVE accounts (status == "Active").
Suspended accounts can't sign in, so they aren't a risk right now.

Each function returns a sorted list of emails (or a dict for the admin check),
so the results are easy to test and to show on a web page later.
"""

import pandas as pd


def active_only(users):
    """Return just the rows where status is "Active"."""
    return users[users["status"] == "Active"]


# ---------------------------------------------------------------------------
# Check 1 - WORKED EXAMPLE (already done). Read it, then use the same pattern.
# ---------------------------------------------------------------------------
def find_inactive_accounts(users, audit_date, days=90):
    """Active accounts with no sign-in for MORE than `days` days.

    An account that has never signed in (last_login is empty) also counts.
    """
    active = active_only(users)
    cutoff = pd.Timestamp(audit_date) - pd.Timedelta(days=days)

    never_logged_in = active["last_login"].isna()
    too_old = active["last_login"] < cutoff

    inactive = active[never_logged_in | too_old]
    return sorted(inactive["email"])


# ---------------------------------------------------------------------------
# Check 2 - YOUR TURN
# ---------------------------------------------------------------------------
def find_users_without_mfa(users):
    """Active accounts where mfa_enrolled is False.

    Hint: start from active_only(users), then filter on the mfa_enrolled column.
    The ~ operator flips True/False in pandas:  df[~df["col"]]
    """
    active = active_only(users)
    return sorted(active[~active["mfa_enrolled"]]["email"])
# ---------------------------------------------------------------------------
# Check 3 - YOUR TURN
# ---------------------------------------------------------------------------
def find_orphaned_accounts(users, roster):
    """Active accounts whose email is NOT on the HR roster
    (people who left the company but still have an account).

    Hints:
    - Look closely at the roster: one email has capital letters.
      Clean the roster emails with .str.strip().str.lower() before comparing.
    - pandas .isin() checks whether each value is in a list:
          df["email"].isin(some_list)
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Check 4 - YOUR TURN
# ---------------------------------------------------------------------------
def check_admin_count(users, max_ratio=0.10):
    """Is the share of admins among active accounts too high?

    Return a dict like:
        {
            "admin_count": 5,
            "active_count": 18,
            "ratio": 0.28,        # admin_count / active_count, rounded to 2 decimals
            "too_many": True,     # ratio > max_ratio
            "admins": [...],      # sorted list of admin emails
        }
    """
    raise NotImplementedError
