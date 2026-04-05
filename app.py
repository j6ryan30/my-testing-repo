from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from database import init_db, create_users

init_db()
create_users()

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "books.db"
# -----------------------------
# GENERATE BARCODE FROM ISBN
# -----------------------------
import barcode
from barcode.writer import ImageWriter
import os

BARCODE_FOLDER = "static/barcodes"

# Create folder if not exists
if not os.path.exists(BARCODE_FOLDER):
    os.makedirs(BARCODE_FOLDER)


def generate_barcode(isbn):

    barcode_path = os.path.join(
        BARCODE_FOLDER,
        f"{isbn}"
    )

    if not os.path.exists(barcode_path + ".png"):

        code128 = barcode.get(
            "code128",
            isbn,
            writer=ImageWriter()
        )

        code128.save(barcode_path)

    return f"barcodes/{isbn}.png"

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# LOGIN REQUIRED DECORATOR
# (Restrict Routes Based on Role)
# -----------------------------
def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "user_id" not in session:
                flash("Login required.")
                return redirect(url_for("login"))

            if role and session.get("role") != role:
                flash("Access denied.")
                return redirect(url_for("dashboard"))

            return f(*args, **kwargs)

        return decorated_function
    return wrapper


# -----------------------------
# LOGIN PAGE UI
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            # Default role assignment
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        flash("Invalid login credentials.")

    return render_template("login.html")


# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
@login_required()
def dashboard():

    return render_template("dashboard.html")


# -----------------------------
# DISPLAY INVENTORY LIST
# -----------------------------
@app.route("/books")
@login_required()
def books():

    conn = get_db_connection()

    books = conn.execute(
        "SELECT * FROM books ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return render_template("books.html", books=books)


# -----------------------------
# ADD BOOK FORM
# -----------------------------
@app.route("/add_book", methods=["GET", "POST"])
@login_required()
def add_book():

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        quantity = request.form["quantity"]

        # -----------------------------
        # VALIDATE INPUT FIELDS
        # -----------------------------
        if not title or not author:
            flash("Title and Author required.")
            return redirect(url_for("add_book"))

        if int(quantity) < 0:
            flash("Quantity must be positive.")
            return redirect(url_for("add_book"))

        conn = get_db_connection()

        try:

            conn.execute("""
                INSERT INTO books
                (title, author, isbn, quantity)
                VALUES (?, ?, ?, ?)
            """, (title, author, isbn, quantity))

            conn.commit()

            flash("Book added successfully.")

        except sqlite3.IntegrityError:

            flash("ISBN already exists.")

        finally:

            conn.close()

        return redirect(url_for("books"))

    return render_template("add_book.html")


# -----------------------------
# CREATE EDIT BOOK FORM
# -----------------------------
@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
@login_required()
def edit_book(id):

    conn = get_db_connection()

    book = conn.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        isbn = request.form["isbn"]
        quantity = request.form["quantity"]

        # -----------------------------
        # VALIDATE UPDATE INPUTS
        # -----------------------------
        if not title or not author:
            flash("Fields required.")
            return redirect(url_for("edit_book", id=id))

        conn.execute("""
            UPDATE books
            SET title=?,
                author=?,
                isbn=?,
                quantity=?
            WHERE id=?
        """, (title, author, isbn, quantity, id))

        conn.commit()
        conn.close()

        flash("Book updated.")

        return redirect(url_for("books"))

    conn.close()

    return render_template("edit_book.html", book=book)


# -----------------------------
# DELETE BOOK
# -----------------------------
@app.route("/delete_book/<int:id>")
@login_required(role="admin")
def delete_book(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Book deleted.")

    return redirect(url_for("books"))


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("login"))
# -----------------------------
# GENERATE BARCODE FROM ISBN
# -----------------------------



# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":

   

    app.run(debug=True)