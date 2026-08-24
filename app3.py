from flask import Flask, request, redirect, render_template_string, session
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
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


setup_database()


# =========================
# REGISTER PAGE
# =========================

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no">

<title>Register</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {

    min-height: 100vh;

    font-family: Arial, sans-serif;

    color: white;

    background:
        radial-gradient(
            circle at top,
            #432366,
            #180b2d
        );
}


/* =========================================================
   HEADER
   ========================================================= */

.top {

    height: 260px;

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            rgba(25,5,50,.35),
            rgba(25,5,50,.88)
        ),
        url("https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1200&auto=format&fit=crop");

    background-size: cover;

    background-position: center;
}


.back {

    position: absolute;

    top: 15px;

    left: 18px;

    font-size: 42px;
}


.language {

    position: absolute;

    top: 20px;

    right: 18px;

    font-size: 14px;
}


.logo {

    position: absolute;

    top: 90px;

    width: 100%;

    text-align: center;
}


.logo h1 {

    font-size: 43px;

    font-style: italic;

    color: #b65cff;
}


.logo h2 {

    font-size: 35px;

    color: #ff9d16;
}


/* =========================================================
   REGISTER FORM
   ========================================================= */

.container {

    width: calc(100% - 32px);

    max-width: 430px;

    margin: 15px auto;
}


.message {

    padding: 10px;

    margin-bottom: 12px;

    border-radius: 10px;

    text-align: center;

    color: #ffd75a;

    background:
        rgba(255,255,255,.08);
}


.input-box {

    height: 58px;

    margin-bottom: 13px;

    display: flex;

    align-items: center;

    padding: 0 13px;

    border-radius: 14px;

    border: 1px solid
        rgba(190,145,230,.42);

    background: #2b1846;
}


.icon {

    width: 32px;

    min-width: 32px;

    text-align: center;

    font-size: 19px;
}


.country {

    margin-right: 8px;

    font-size: 18px;

    font-weight: bold;
}


input {

    width: 100%;

    height: 100%;

    min-width: 0;

    border: none;

    outline: none;

    background: transparent;

    color: white;

    font-size: 16px;
}


input::placeholder {

    color: #9d88b7;
}


/* =========================================================
   PASSWORD EYE
   ========================================================= */

.eye {

    width: 30px;

    min-width: 30px;

    height: 30px;

    display: flex;

    align-items: center;

    justify-content: center;

    cursor: pointer;
}


.eye-shape {

    width: 21px;

    height: 13px;

    border: 2px solid #bda5d6;

    border-radius: 80% 20%;

    transform: rotate(45deg);

    position: relative;
}


.eye-shape::after {

    content: "";

    width: 5px;

    height: 5px;

    position: absolute;

    top: 2px;

    left: 6px;

    border-radius: 50%;

    background: #bda5d6;
}


/* =========================================================
   REGISTER BUTTON
   ========================================================= */

.register {

    width: 100%;

    height: 58px;

    margin-top: 20px;

    border: none;

    border-radius: 30px;

    background:
        linear-gradient(
            #ffe66b,
            #efa800
        );

    color: #28132f;

    font-size: 20px;

    cursor: pointer;
}


# =========================
# REGISTER
# =========================

@app.route("/", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        phone = request.form.get(
            "phone", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        confirm_password = request.form.get(
            "confirm_password", ""
        )


        if not phone or not password or not confirm_password:

            message = "Please fill all fields."

        elif password != confirm_password:

            message = "Passwords do not match."

        else:

            try:

                connection = sqlite3.connect(DATABASE)

                connection.execute(
                    """
                    INSERT INTO users
                    (username, phone, password)
                    VALUES (?, ?, ?)
                    """,
                    (
                        username,
                        phone,
                        password
                    )
                )

                connection.commit()
                connection.close()

                return redirect("/login")

            except sqlite3.IntegrityError:

                message = "Account already exists."


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

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial;

    background:
        radial-gradient(
            circle at top,
            #48206d,
            #24113d 50%,
            #14091f
        );

    color: white;
    padding: 40px 20px;
}

.box {
    max-width: 400px;
    margin: auto;

    background: rgba(42,20,67,.9);

    padding: 28px;
    border-radius: 20px;
}

h2 {
    text-align: center;
    color: #e0b24f;
}

input {
    width: 100%;
    padding: 14px;
    margin: 10px 0;

    border-radius: 10px;
    border: 1px solid #8d65ae;

    background: #24113d;
    color: white;

    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 14px;

    background: #ffb600;
    color: #251530;

    border: none;
    border-radius: 10px;

    font-size: 18px;
}

a {
    display: block;
    margin-top: 18px;
    text-align: center;
    color: #e4b54e;
}

.message {
    color: #ff7777;
    text-align: center;
}

</style>

</head>

<body>

<div class="box">

<h2>Password Login</h2>

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

<p class="message">
{{ message }}
</p>

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

        username = request.form.get(
            "username", ""
        )

        password = request.form.get(
            "password", ""
        )


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

            if user["password"] == password:

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

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial;

    background:
        radial-gradient(
            circle at top,
            #48206d,
            #24113d 50%,
            #14091f
        );

    padding: 40px 20px;
}

.box {
    max-width: 400px;
    margin: auto;

    background: rgba(42,20,67,.9);

    padding: 28px;
    border-radius: 20px;
}

h2 {
    text-align: center;
    color: #e0b24f;
}

input {
    width: 100%;
    padding: 14px;
    margin: 10px 0;

    box-sizing: border-box;

    background: #24113d;
    color: white;

    border: 1px solid #8d65ae;
    border-radius: 10px;
}

button {
    width: 100%;
    padding: 14px;

    background: #ffb600;
    color: #251530;

    border: none;
    border-radius: 10px;

    font-size: 18px;
}

.error {
    color: #ff7777;
    text-align: center;
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

<p class="error">
{{ message }}
</p>

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

        admin_id = request.form.get(
            "admin_id", ""
        )

        admin_password = request.form.get(
            "admin_password", ""
        )


        if (
            admin_id == ADMIN_ID
            and
            admin_password == ADMIN_PASSWORD
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
        SELECT id, username, phone, password
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

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

body {
    font-family: Arial;

    background:
        radial-gradient(
            circle at top,
            #48206d,
            #24113d 50%,
            #14091f
        );

    color: white;

    padding: 25px 15px;
}

h1 {
    text-align: center;
    color: #e4b54e;
}

.user {
    background: #24133b;

    padding: 20px;

    margin: 15px auto;

    max-width: 500px;

    border-radius: 15px;

    border: 1px solid #76538e;
}

.user p {
    margin: 12px 0;
}

.password {
    color: #ff7777;
    font-weight: bold;
}

.logout {
    display: block;

    width: 160px;

    margin: 0 auto 25px;

    padding: 12px;

    text-align: center;

    background: #ffb600;
    color: #241530;

    text-decoration: none;

    border-radius: 20px;
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

            <p class="password">
                <b>Password:</b>
                {{ user["password"] }}
            </p>

        </div>

    {% endfor %}

{% else %}

    <p style="text-align:center;">
        No registered users yet.
    </p>

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

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect("/admin")


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
