from flask import Flask, request, redirect, render_template
import sqlite3
from datetime import date

app = Flask(__name__)
DB_FILE = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.execute("SELECT id, description, amount, category, date FROM expenses ORDER BY id DESC")
    expenses = cur.fetchall()
    total = sum(e[2] for e in expenses)
    conn.close()
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/add", methods=["POST"])
def add_expense():
    description = request.form.get("description")
    amount = request.form.get("amount")
    category = request.form.get("category")
    today = date.today().isoformat()

    if description and amount and category:
        conn = sqlite3.connect(DB_FILE)
        conn.execute(
            "INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
            (description, float(amount), category, today)
        )
        conn.commit()
        conn.close()
    return redirect("/")
@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
