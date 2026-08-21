from flask import Flask, request, redirect, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "demo-secret-key-change-this"

DATABASE = "users.db"

# =========================
# ADMIN LOGIN DETAILS
# =========================

ADMIN_ID = "Hadi"
ADMIN_PASSWORD = "hadi1010"


# =========================
# DATABASE
# =========================

def setup_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


setup_database()


# =========================
# REGISTER PAGE
# =========================

REGISTER_PAGE = """
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

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 12px;
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
"""


# =========================
# REGISTER
# =========================

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

                connection = sqlite3.connect(DATABASE)

                connection.execute(
                    """
                    INSERT INTO users
                    (username, phone, password_hash)
                    VALUES (?, ?, ?)
                    """,
                    (username, phone, password_hash)
                )

                connection.commit()
                connection.close()

                return redirect("/login")

            except sqlite3.IntegrityError:

                message = "Username already exists."

    return render_template_string(
        REGISTER_PAGE,
        message=message
    )


# =========================
# USER LOGIN PAGE
# =========================

LOGIN_PAGE = """
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

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 12px;
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

    <h2>User Login</h2>

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
        Create Account
    </a>

</div>

</body>
</html>
"""


# =========================
# USER LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        connection = sqlite3.connect(DATABASE)
        connection.row_factory = sqlite3.Row

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        connection.close()

        if user:

            if check_password_hash(
                user["password_hash"],
                password
            ):

                message = "Login successful!"

            else:

                message = "Wrong password."

        else:

            message = "Username not found."

    return render_template_string(
        LOGIN_PAGE,
        message=message
    )


# =========================
# ADMIN LOGIN PAGE
# =========================

ADMIN_LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>

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

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 12px;
            background: black;
            color: white;
            border: none;
            border-radius: 6px;
        }

        .error {
            color: red;
        }
    </style>
</head>

<body>

<div class="box">

    <h2>Admin Login</h2>

    <form method="POST">

        <input
            type="text"
            name="admin_id"
            placeholder="Admin ID"
            required
        >

        <input
            type="password"
            name="admin_password"
            placeholder="Admin Password"
            required
        >

        <button type="submit">
            Admin Login
        </button>

    </form>

    <p class="error">{{ message }}</p>

</div>

</body>
</html>
"""


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin_login():

    if session.get("admin_logged_in"):
        return redirect("/admin/users")

    message = ""

    if request.method == "POST":

        admin_id = request.form.get("admin_id", "")
        admin_password = request.form.get(
            "admin_password",
            ""
        )

        if (
            admin_id == ADMIN_ID
            and admin_password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect("/admin/users")

        else:

            message = "Invalid Admin ID or Password."

    return render_template_string(
        ADMIN_LOGIN_PAGE,
        message=message
    )


# =========================
# REGISTERED USERS PAGE
# =========================

@app.route("/admin/users")
def admin_users():

    if not session.get("admin_logged_in"):
        return redirect("/admin")

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    users = connection.execute(
        """
        SELECT id, username, phone
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template_string(
        """
<!DOCTYPE html>
<html>

<head>

    <title>Registered Users</title>

    <style>

        body {
            font-family: Arial;
            background: #eeeeee;
            padding: 30px;
        }

        .user {
            background: white;
            padding: 20px;
            margin: 15px auto;
            max-width: 500px;
            border-radius: 10px;
        }

        .logout {
            display: inline-block;
            margin-bottom: 20px;
        }

    </style>

</head>

<body>

<h1>Registered Users</h1>

<a class="logout" href="/admin/logout">
    Admin Logout
</a>

{% if users %}

    {% for user in users %}

        <div class="user">

            <p>
                <b>User ID:</b>
                {{ user["id"] }}
            </p>

            <p>
                <b>Username:</b>
                {{ user["username"] }}
            </p>

            <p>
                <b>Phone:</b>
                {{ user["phone"] }}
            </p>

            <p>
                <b>Password:</b>
                ********
            </p>

        </div>

    {% endfor %}

{% else %}

    <p>No registered users yet.</p>

{% endif %}

</body>

</html>
        """,
        users=users
    )


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin")


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
