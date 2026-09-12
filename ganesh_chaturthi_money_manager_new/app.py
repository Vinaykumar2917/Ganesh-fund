from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
DB = BASE / "money.db"

app = Flask(__name__)

def db():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = db()
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY id DESC"
    ).fetchall()
    conn.close()

    added = sum(r["amount"] for r in rows if r["kind"] == "added")
    expenses = sum(r["amount"] for r in rows if r["kind"] == "expense")
    balance = added - expenses

    return render_template(
        "index.html",
        transactions=rows,
        added=added,
        expenses=expenses,
        balance=balance
    )

@app.post("/add")
def add_transaction():
    kind = request.form.get("kind", "added")
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0

    note = request.form.get("note", "").strip() or (
        "Money Added" if kind == "added" else "Expense"
    )

    if amount <= 0:
        return redirect(url_for("index"))

    conn = db()
    conn.execute(
        "INSERT INTO transactions(kind, amount, note, created_at) VALUES (?, ?, ?, ?)",
        (kind, amount, note, datetime.now().strftime("%d-%m-%Y %I:%M %p"))
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.post("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    conn = db()
    conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.post("/clear")
def clear_all():
    conn = db()
    conn.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.get("/api/summary")
def summary():
    conn = db()
    rows = conn.execute("SELECT kind, amount FROM transactions").fetchall()
    conn.close()
    added = sum(r["amount"] for r in rows if r["kind"] == "added")
    expenses = sum(r["amount"] for r in rows if r["kind"] == "expense")
    return jsonify(added=added, expenses=expenses, balance=added-expenses)

if __name__ == "__main__":
    init_db()
    print("\nGanesh Chaturthi Money Manager")
    print("Open: http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
