from flask import Flask, request, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "lior!23"  # חובה לשנות בפרודקשן

DB_PATH = Path("auth.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.before_request
def _ensure_db():
    if not DB_PATH.exists():
        init_db()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = get_db()
    row = conn.execute("SELECT id, username FROM users WHERE id = ?", (uid,)).fetchone()
    conn.close()
    return dict(row) if row else None


@app.get("/")
def home():
    user = current_user()
    if user:
        return f"Hello, {user['username']}! Go to /me or /logout"
    return "Hello! Go to /register or /login"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return """
        <h2>Register</h2>
        <form method="post">
          <input name="username" placeholder="username" required />
          <input name="password" placeholder="password" type="password" required />
          <button type="submit">Create account</button>
        </form>
        """

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    if len(username) < 3:
        return "Username must be at least 3 chars", 400
    if len(password) < 6:
        return "Password must be at least 6 chars", 400

    pw_hash = generate_password_hash(password)  # כולל salt, אלגוריתם חזק
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, pw_hash),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username already exists", 409
    finally:
        conn.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <h2>Login</h2>
        <form method="post">
          <input name="username" placeholder="username" required />
          <input name="password" placeholder="password" type="password" required />
          <button type="submit">Login</button>
        </form>
        """

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""

    conn = get_db()
    row = conn.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()

    if not row:
        return "Invalid username or password", 401

    if not check_password_hash(row["password_hash"], password):
        return "Invalid username or password", 401

    # התחברות הצליחה
    session["user_id"] = row["id"]
    return redirect(url_for("me"))


@app.get("/me")
def me():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    return jsonify(user)


@app.get("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

