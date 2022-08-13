from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, session
from datetime import datetime
from pytz import timezone
import sqlite3

auth = Blueprint('auth', __name__)

# con = sqlite3.connect("todo.db")
# con.row_factory = sqlite3.Row  
# cur = con.cursor()

def myDb():

    con = sqlite3.connect("todo.db")

    return con

@auth.route("/signup", methods=['POST','GET'])
def signUp():

    con  = myDb()
    con.row_factory = sqlite3.Row  
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

    con  = myDb()
    con.row_factory = sqlite3.Row  
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
            return redirect(url_for("auth.myToDoList"))
    
    return render_template("login.html")



@auth.route("/mytodolist")
def myToDoList():
    
    if "user" in session:

        con  = myDb()
        con.row_factory = sqlite3.Row  
        cur = con.cursor()

        username = session["user"]

        cur.execute("SELECT * FROM User where username=?",([username]))
        user = cur.fetchall()

        cur.execute("SELECT * FROM ToDO where username=?",([username]))
        todo = cur.fetchall()

        return render_template("dashboard.html", user=user, todo=todo )
    
    else:
        return redirect(url_for("auth.login"))


@auth.route("/add-todo", methods=['POST', 'GET'])
def addToDo():

    if "user" in session:

        con  = myDb()
        con.row_factory = sqlite3.Row  
        cur = con.cursor()

        if request.method == 'POST':
            username = session["user"]
            todoName = request.form.get('todoName')

            time_format = "%B %d, %Y %I:%M%p"
            now = datetime.now().strftime(time_format)
            tz = ['Asia/Manila']

            for zone in tz:
                date = datetime.now(timezone(zone)).strftime(time_format)

            cur.execute("INSERT into ToDo (todo_name, date, username) values (?,?,?)",(todoName, date, username))
            con.commit()

            flash("Successfully Added!",category='success')
            return redirect(url_for('auth.myToDoList'))

        return render_template("dashboard.html")
    
    else:
        return redirect(url_for("auth.login"))

@auth.route("/delete-todo/<int:id>")
def deleteToDo(id):

    if "user" in session:

        try:
            con  = myDb()
            con.row_factory = sqlite3.Row  
            cur = con.cursor()

            cur.execute("DELETE FROM ToDo where todo_id=?",([id]))
            con.commit()

            flash("Record Deleted Successfully",category='success')

        except:
            flash("Record Delete Failed","danger",category="error")

        finally:
            return redirect(url_for("auth.myToDoList"))
    
    else:
        return redirect(url_for("auth.login"))

@auth.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for('auth.login'))
