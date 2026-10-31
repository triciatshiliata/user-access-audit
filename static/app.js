// Front end: send the files to the Flask API and show the results.

let currentReport = null;

// ---------------------------------------------------------------------------
// YOUR TURN (Part C)
// ---------------------------------------------------------------------------
// Fill a <ul> on the page with one <li> per email.
//   listId: the id of the <ul>, e.g. "inactive-list"
//   emails: an array of email strings, e.g. ["ben@x.com", "kara@x.com"]
//
// Steps:
//   1. Find the <ul>:              const list = document.getElementById(listId);
//   2. Empty it first:             list.innerHTML = "";
//   3. If emails is empty (emails.length === 0):
//        make one <li> that says "None found", give it the class "none"
//        (li.className = "none"), add it, and stop (return).
//   4. Otherwise, loop over emails (for (const email of emails) { ... })
//        and for each one: create an <li>, set its text, add it to the list.
//
// Useful pieces:
//   const li = document.createElement("li");   // make a new <li>
//   li.textContent = "some text";              // set its text
//   list.appendChild(li);                      // put it inside the <ul>
function renderList(listId, emails) {
  // write your code here
}

// ---------------------------------------------------------------------------
// Everything below is done - read it to see how the page works.
// ---------------------------------------------------------------------------

function showReport(report) {
  currentReport = report;

  document.getElementById("total-accounts").textContent = report.total_accounts;
  document.getElementById("active-accounts").textContent = report.active_accounts;
  document.getElementById("issue-count").textContent = report.accounts_with_issues;
  document.getElementById("admin-ratio").textContent = Math.round(report.admins.ratio * 100) + "%";
  document.getElementById("admin-stat").classList.toggle("alert", report.admins.too_many);
  document.getElementById("audit-date").textContent = report.audit_date;

  renderList("inactive-list", report.inactive);
  renderList("no-mfa-list", report.no_mfa);
  renderList("orphaned-list", report.orphaned);
  renderList("admins-list", report.admins.admins);

  document.getElementById("results").hidden = false;
}

function showError(message) {
  const error = document.getElementById("error");
  error.textContent = message;
  error.hidden = !message;
}

async function handleResponse(response) {
  const data = await response.json();
  if (!response.ok) {
    showError(data.error || "Something went wrong.");
    return;
  }
  showError("");
  showReport(data);
}

// "Run audit": send both files to the API
document.getElementById("upload-form").addEventListener("submit", async (event) => {
  event.preventDefault(); // stop the browser from reloading the page
  const formData = new FormData(event.target);
  const response = await fetch("/api/audit", { method: "POST", body: formData });
  handleResponse(response);
});

// "Try it with sample data"
document.getElementById("sample-button").addEventListener("click", async () => {
  const response = await fetch("/api/sample");
  handleResponse(response);
});

// "Download report (CSV)": build the file in the browser
document.getElementById("download-button").addEventListener("click", () => {
  if (!currentReport) return;

  const rows = [["issue", "email"]];
  for (const email of currentReport.inactive) rows.push(["Inactive 90+ days", email]);
  for (const email of currentReport.no_mfa) rows.push(["No MFA", email]);
  for (const email of currentReport.orphaned) rows.push(["Left the company", email]);
  for (const email of currentReport.admins.admins) rows.push(["Admin account", email]);

  const csv = rows.map((row) => row.join(",")).join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `access-audit-${currentReport.audit_date}.csv`;
  link.click();
});
