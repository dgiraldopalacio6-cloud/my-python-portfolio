from flask import Flask, render_template, url_for

app = Flask(__name__)

# Store only the static filename at import time
PROJECTS = [
    {
        "id": "inventory-audit",
        "title": "Inventory Audit & Traceability",
        "short": "Event-driven inventory with after-commit workers and audit trails.",
        "description": "Architected an event-sourced inventory pipeline that records per-row modifications and supplier provenance.",
        "tech": ["Python", "Flask", "SQLAlchemy", "Celery", "Postgres"],
        "repo": "https://github.com/yourusername/inventory-audit",
        "screenshot_file": "screenshots/inventory.png"
    },
    # other projects...
]

@app.route("/")
def index():
    # Convert filenames to URL paths inside a request (application) context
    projects = []
    for p in PROJECTS:
        p2 = p.copy()
        p2["screenshot"] = url_for("static", filename=p.get("screenshot_file", "screenshots/placeholder.png"))
        projects.append(p2)
    return render_template("index.html", projects=projects)

if __name__ == "__main__":
    app.run(debug=True)