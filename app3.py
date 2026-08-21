from flask import Flask, request, redirect, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

DATABASE = "users.db"


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


REGISTER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>

<body>

<h1>Create Account</h1>

<form method="POST">

    <p>
        <input type="text"
               name="username"
               placeholder="Username"
               required>
    </p>

    <p>
        <input type="text"
               name="phone"
               placeholder="Phone Number"
               required>
    </p>

    <p>
        <input type="password"
               name="password"
               placeholder="Password"
               required>
    </p>

    <p>
        <button type="submit">Register</button>
    </p>

</form>

<p>{{ message }}</p>

<a href="/login">Already registered? Login</a>

</body>
</html>
"""


LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>

<body>

<h1>Login</h1>

<form method="POST">

    <p>
        <input type="text"
               name="username"
               placeholder="Username"
               required>
    </p>

    <p>
        <input type="password"
               name="password"
               placeholder="Password"
               required>
    </p>

    <p>
        <button type="submit">Login</button>
    </p>

</form>

<p>{{ message }}</p>

<a href="/">Create Account</a>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        phone = request.form["phone"]
        password = request.form["password"]

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

            message = "This username already exists."

    return render_template_string(
        REGISTER_HTML,
        message=message
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect(DATABASE)
        connection.row_factory = sqlite3.Row

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user is not None:

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
        LOGIN_HTML,
        message=message
    )


@app.route("/admin")
def admin():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    users = connection.execute(
        """
        SELECT username, phone
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin</title>
    </head>

    <body>

    <h1>Registered Demo Users</h1>

    {% for user in users %}

        <hr>

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

    {% endfor %}

    </body>
    </html>
    """

    return render_template_string(
        html,
        users=users
    )


if __name__ == "__main__":

    setup_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
