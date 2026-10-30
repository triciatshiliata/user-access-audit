"""Load the user export and HR roster CSV files into pandas DataFrames."""

import pandas as pd


def load_users(path):
    """Read the user export CSV.

    Columns: email, first_name, last_name, department, status,
             is_admin, mfa_enrolled, last_login

    - is_admin and mfa_enrolled become True/False
    - last_login becomes a date (empty = the user never logged in -> NaT)
    """
    users = pd.read_csv(path)
    users["email"] = users["email"].str.strip().str.lower()
    users["status"] = users["status"].str.strip()
    for col in ["is_admin", "mfa_enrolled"]:
        users[col] = users[col].astype(str).str.strip().str.upper() == "TRUE"
    users["last_login"] = pd.to_datetime(users["last_login"], errors="coerce")
    return users


def load_roster(path):
    """Read the HR roster CSV (one row per current employee).

    Columns: email, full_name, department
    Emails are NOT cleaned here on purpose - see find_orphaned_accounts.
    """
    return pd.read_csv(path)
