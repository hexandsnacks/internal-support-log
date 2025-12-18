from flask import Flask, render_template, request
from flask import redirect
from datetime import datetime
app = Flask(__name__)
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("issues.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db_connection()
    issues = conn.execute("SELECT * FROM issues ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("index.html", issues=issues)

@app.route("/log", methods=["POST"])
def log_issue():
    summary = request.form["summary"]
    details = request.form["details"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO issues (summary, details, timestamp) VALUES (?, ?, ?)",
        (summary, details, timestamp)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_issue(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM issues WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
