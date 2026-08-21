from flask import Flask, request, redirect, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("users.db")

# Database create
conn = db()
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    phone TEXT,
    password_hash TEXT
)
""")
conn.commit()
conn.close()


# Register page
@app.route("/", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        phone = request.form["phone"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        try:
            conn = db()

            conn.execute(
                "INSERT INTO users (username, phone, password_hash) VALUES (?, ?, ?)",
                (username, phone, password_hash)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:
            message = "Username already exists."

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register</title>

        <style>
            body {
                font-family: Arial;
                background: #eeeeee;
                padding: 40px;
            }

            .box {
                max-width: 400px;
                margin: auto;
                background: white;
                padding: 25px;
                border-radius: 12px;
            }

            input, button {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                box-sizing: border-box;
            }

            button {
                background: black;
                color: white;
                border: none;
            }
        </style>
    </head>

    <body>

    <div class="box">

        <h2>Create Account</h2>

        <form method="POST">

            <input
                name="username"
                placeholder="Username"
                required
            >

            <input
                name="phone"
                placeholder="Phone Number"
                required
            >

            <input
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <button type="submit">
                Register
            </button>

        </form>

        <p>{{ message }}</p>

        <a href="/login">
            Already registered? Login
        </a>

    </div>

    </body>
    </html>
    """, message=message)


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user[3],
            password
        ):
            message = "Login successful!"

        else:
            message = "Wrong username or password."

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>

    <body>

    <h2>Login</h2>

    <form method="POST">

        <input
            name="username"
            placeholder="Username"
            required
        >

        <br><br>

        <input
            type="password"
            name="password"
            placeholder="Password"
            required
        >

        <br><br>

        <button type="submit">
            Login
        </button>

    </form>

    <p>{{ message }}</p>

    <a href="/">
        Register
    </a>

    </body>
    </html>
    """, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
