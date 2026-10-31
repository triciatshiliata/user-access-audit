# User Access Audit

A tool that scans a company's user account export (Google Workspace or Microsoft 365) and flags security risks that IT teams look for during audits, onboarding/offboarding reviews and acquisitions.

> 🚧 **In progress:** the command-line version is being built now. Web app, CI and deployment come next.

## What it checks

| Check | Why it matters |
|---|---|
| **Inactive accounts** (no sign-in for 90+ days) | Unused accounts are easy targets because nobody notices if they're taken over |
| **Accounts without MFA** | A stolen password is enough to get in |
| **Accounts of people who left** (not on the HR roster) | Former employees should lose access the day they leave |
| **Too many admins** | Every admin account widens the damage a single breach can do |

Suspended accounts are skipped, since they can't sign in.

## Run it

```bash
pip install -r requirements.txt
python -m audit.cli sample_data/users.csv sample_data/hr_roster.csv
pytest
```

## Sample data

`sample_data/` contains a made-up company (`brightpath.example`) with 20 accounts and an HR roster. Every person in it is fictional.

## Roadmap

- [x] Load and clean the user export and HR roster
- [x] Check: inactive accounts
- [x] Check: accounts without MFA
- [x] Check: accounts of people who left
- [x] Check: admin count
- [ ] Web app: upload CSVs, see results on a dashboard, download the report
- [ ] GitHub Actions: run tests on every push
- [ ] Deploy with a public link

## Tech stack

Python · pandas · pytest

## Author

**Patricia Tshiliata** · [LinkedIn](https://www.linkedin.com/in/patricia-tshiliata) · [GitHub](https://github.com/triciatshiliata)
