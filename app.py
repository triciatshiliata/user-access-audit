"""Web app: upload the two CSV files and get the audit back as JSON.

Run it with:   python app.py
Then open:     http://127.0.0.1:5000
"""

from datetime import date
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from audit.loader import load_roster, load_users
from audit.report import build_report

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # refuse uploads over 2 MB

SAMPLE_DATA = Path(__file__).parent / "sample_data"


@app.get("/")
def home():
    """Serve the web page (templates/index.html)."""
    return render_template("index.html")


@app.post("/api/audit")
def audit_uploaded_files():
    """Run the audit on the two CSV files the user uploaded."""
    users_file = request.files.get("users")
    roster_file = request.files.get("roster")

    if not users_file or not roster_file:
        return jsonify(error="Please upload both CSV files."), 400

    try:
        users = load_users(users_file)
        roster = load_roster(roster_file)
        report = build_report(users, roster, date.today())
    except Exception:
        return jsonify(error="Couldn't read those files. Check that they have the expected columns."), 400

    return jsonify(report)


# ---------------------------------------------------------------------------
# YOUR TURN (Part B)
# ---------------------------------------------------------------------------
# Write a route for the "Try it with sample data" button:
#   - URL: /api/sample   - method: GET   (use @app.get, like home() above)
#   - load sample_data/users.csv and sample_data/hr_roster.csv
#     (hint: SAMPLE_DATA / "users.csv" builds the path)
#   - build the report for today's date and return it with jsonify(...)
# It's a shorter version of audit_uploaded_files - no upload, no error checks.


if __name__ == "__main__":
    app.run(debug=True)
