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

REGISTER_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;

            background:
                radial-gradient(
                    circle at top,
                    #48206d 0%,
                    #24113d 45%,
                    #14091f 100%
                );

            color: white;
            padding: 25px 18px 40px;
        }

        .page {
            width: 100%;
            max-width: 430px;
            margin: auto;
        }

        .back {
            font-size: 42px;
            color: white;
            text-decoration: none;
            display: inline-block;
            margin-bottom: 5px;
        }

        .header {
            text-align: center;
            padding: 35px 10px 30px;
        }

        .header h1 {
            margin: 0;
            font-size: 48px;
            font-weight: 800;
            font-style: italic;
            color: #b76cff;
            text-shadow:
                0 0 10px rgba(183,108,255,.5);
        }

        .header h2 {
            margin: -2px 0 0;
            font-size: 34px;
            color: #ffae19;
            font-style: italic;
        }

        .form-box {
            width: 100%;
        }

        .input-box {
            width: 100%;
            height: 72px;
            margin-bottom: 20px;

            display: flex;
            align-items: center;

            padding: 0 18px;

            border: 1px solid rgba(190,150,255,.45);
            border-radius: 18px;

            background:
                rgba(42, 20, 67, .88);

            box-shadow:
                inset 0 0 15px rgba(0,0,0,.12);
        }

        .icon {
            width: 42px;
            font-size: 24px;
            color: #c9a7ff;
            text-align: center;
        }

        .input-box input {
            flex: 1;
            min-width: 0;

            border: none;
            outline: none;
            background: transparent;

            color: white;
            font-size: 20px;
            padding-left: 12px;
        }

        .input-box input::placeholder {
            color: #a99bb9;
        }

        .show {
            cursor: pointer;
            color: #c5a8e8;
            font-size: 20px;
            padding-left: 8px;
        }

        .register-btn {
            width: 100%;
            height: 68px;

            margin-top: 18px;

            border: none;
            border-radius: 40px;

            background:
                linear-gradient(
                    180deg,
                    #ffe66b,
                    #ffb300
                );

            color: #281634;
            font-size: 25px;
            font-weight: 600;

            cursor: pointer;

            box-shadow:
                0 6px 15px rgba(0,0,0,.25);
        }

        .register-btn:active {
            transform: scale(.98);
        }

        .login-btn {
            width: 100%;
            height: 68px;

            margin-top: 28px;

            border: 1px solid #d8a83f;
            border-radius: 40px;

            background: transparent;

            color: #e7b84d;
            font-size: 23px;

            cursor: pointer;
        }

        .message {
            text-align: center;
            min-height: 24px;
            margin: 14px 0 0;
            color: #ff7676;
            font-size: 15px;
        }

        .bottom-space {
            height: 20px;
        }

    </style>
</head>


<body>

<div class="page">

    <a class="back" href="/login">‹</a>

    <div class="header">
        <h1>Register</h1>
        <h2>Create Account</h2>
    </div>


    <div class="form-box">

        <form method="POST">

            <!-- PHONE -->

            <div class="input-box">

                <div class="icon">📱</div>

                <input
                    type="tel"
                    name="phone"
                    placeholder="Enter your phone number"
                    required
                >

            </div>


            <!-- PASSWORD -->

            <div class="input-box">

                <div class="icon">🔒</div>

                <input
                    id="password"
                    type="password"
                    name="password"
                    placeholder="Password"
                    required
                >

                <div
                    class="show"
                    onclick="togglePassword('password')"
                >
                    ◉
                </div>

            </div>


            <!-- CONFIRM PASSWORD -->

            <div class="input-box">

                <div class="icon">🔒</div>

                <input
                    id="confirm_password"
                    type="password"
                    name="confirm_password"
                    placeholder="Enter the password again"
                    required
                >

                <div
                    class="show"
                    onclick="togglePassword('confirm_password')"
                >
                    ◉
                </div>

            </div>


            <!-- USERNAME IS KEPT INTERNALLY
                 SO THE EXISTING DATABASE STRUCTURE
                 DOES NOT HAVE TO CHANGE -->

            <input
                type="hidden"
                name="username"
                id="username"
            >


            <button
                class="register-btn"
                type="submit"
            >
                Register
            </button>

        </form>


        <p class="message">
            {{ message }}
        </p>


        <button
            class="login-btn"
            onclick="window.location.href='/login'"
        >
            Password Login
        </button>

    </div>

    <div class="bottom-space"></div>

</div>


<script>

function togglePassword(id) {

    const input = document.getElementById(id);

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}


/*
    Generate an internal username from phone number.
    This keeps the existing SQLite database structure.
*/

document.querySelector("form").addEventListener(
    "submit",
    function () {

        const phone =
            document.querySelector(
                'input[name="phone"]'
            ).value.trim();

        document.getElementById("username").value =
            "user_" + phone.replace(/[^0-9]/g, "");

    }
);

</script>

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
