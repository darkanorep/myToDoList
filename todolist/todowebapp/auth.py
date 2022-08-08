from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, session
import sqlite3

auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['POST','GET'])
def signUp():

    with sqlite3.connect("todo.db") as con:
        cur = con.cursor()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        statement = f"SELECT * FROM User WHERE username='{username}';"
        cur.execute(statement)
        data = cur.fetchone()

        if data:
            flash("This email was already taken.", category='error')
        
        else:
            cur.execute("INSERT into User (username, password, confirmPassword) values (?,?,?)",(username, password, confirmPassword))
            con.commit()

            flash("Successfully registered.", category='success')
            return redirect(url_for("auth.login"))

    return render_template("signup.html")

@auth.route("/login", methods=['GET', 'POST'])
def login():

    with sqlite3.connect("todo.db") as con:
        cur = con.cursor()

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        statement = f"SELECT * FROM User WHERE username='{username}' AND password='{password}';"
        cur.execute(statement)

        if not cur.fetchone():
            flash("Your username or password was incorrect.", category='error')    
            return redirect(url_for("auth.login"))
        
        else: 
            session["user"] = username
            return redirect(url_for("auth.mytodolist"))
    
    return render_template("login.html")


@auth.route("mytodolist")
def mytodolist():

    return render_template("mytodolist.html")


