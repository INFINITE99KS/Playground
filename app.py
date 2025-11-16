import os
import datetime
import time
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Configure application
app = Flask (__name__)

# Configuring sessions,
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "ultima_tryingout"
Session(app)

# Configuring the database.
db = SQL("sqlite:///playground.db")

@app.route("/")
@login_required
def index():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id if it's a GET request from a logged-in user
    if request.method == "GET":
        session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("⚠️ You must provide a username.", "warning")
            # Render the template again instead of redirecting
            return render_template("landing.html")

        elif not password:
            flash("⚠️ You must provide a password.", "warning")
            # Render the template again
            return render_template("landing.html")

        # Query database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Validate username/password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("❌ Invalid username or password.", "danger")
            # Render the template again
            return render_template("landing.html")

        # Remember user
        session["user_id"] = rows[0]["id"]

        flash("✅ Logged in successfully!", "success")
        return redirect("/")

    # User reached route via GET
    else:
        # Just render the login form.
        # The "Welcome aboard!" message is better suited for a homepage or after registration.
        return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("⚠️ Username left empty", "warning")
            return redirect("/register")

        if not password:
            flash("⚠️ Password left empty.", "warning")
            return redirect("/register")

        if password != confirmation:
            flash("⚠️ Password mismatch.", "warning")
            return redirect("/register")

        password_hash = generate_password_hash(password, method='scrypt', salt_length=16)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        except ValueError:
            flash("❌ User already exists.", "danger")
            return redirect("/register")

        flash("✅ User created successfully! Please log in.", "success")
        return redirect("/")
    else:
        return render_template("landing.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/tic")
@login_required
def tic():
    return render_template("xo.html")

@app.route("/trivia")
@login_required
def trivia():
    return render_template("trivia.html")

@app.route("/snake")
@login_required
def snake():
    return render_template("snake.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Reset user password"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("⚠️ Username left empty", "warning")
            return redirect("/forgot")

        if not password:
            flash("⚠️ Password left empty.", "warning")
            return redirect("/forgot")

        if password != confirmation:
            flash("⚠️ Password mismatch.", "warning")
            return redirect("/forgot")

        # Check if user exists
        check_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not check_user:
            flash("❌ No such user exists.", "danger")
            return redirect("/forgot")

        # Update password
        pass_hash = generate_password_hash(password, method='scrypt', salt_length=16)
        db.execute("UPDATE users SET hash = ? WHERE username = ?", pass_hash, username)

        flash("✅ Password updated successfully! Please log in.", "success")
        return redirect("/")

    else: # GET request
        return render_template("forgot.html")
