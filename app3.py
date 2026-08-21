from flask import Flask, request, redirect, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not username or not phone or not password:
            message = "Please fill all fields."

        else:
            password_hash = generate_password_hash(password)

            try:
                conn = get_db()

                conn.execute(
                    """
                    INSERT INTO users
                    (username, phone, password_hash)
                    VALUES (?, ?, ?)
                    """,
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
            margin-top: 12px;
            box-sizing: border-box;
        }

        button {
            background: black;
            color: white;
            border: none;
            border-radius: 6px;
        }

        a {
            display: block;
            margin-top: 15px;
        }
    </style>
</head>

<body>

<div class="box">

    <h2>Create Account</h2>

    <form method="POST">

        <input
            type="text"
            name="username"
            placeholder="Username"
            required
        >

        <input
            type="tel"
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


@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password_hash"],
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
            margin-top: 12px;
            box-sizing: border-box;
        }

        button {
            background: black;
            color: white;
            border: none;
            border-radius: 6px;
        }
    </style>
</head>

<body>

<div class="box">

    <h2>Login</h2>

    <form method="POST">

        <input
            type="text"
            name="username"
            placeholder="Username"
            required
        >

        <input
            type="password"
            name="password"
            placeholder="Password"
            required
        >

        <button type="submit">
            Login
        </button>

    </form>

    <p>{{ message }}</p>

    <a href="/">
        Create new account
    </a>

</div>

</body>
</html>
""", message=message)


@app.route("/admin")
def admin():

    conn = get_db()

    users = conn.execute(
        """
        SELECT username, phone
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Admin</title>
</head>

<body>

<h1>Registered Demo Users</h1>

{% for user in users %}

<div>
    <b>Username:</b> {{ user["username"] }}<br>
    <b>Phone:</b> {{ user["phone"] }}<br>
    <b>Password:</b> ********
</div>

<hr>

{% endfor %}

</body>
</html>
""")


if __name__ == "__main__":

    create_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
