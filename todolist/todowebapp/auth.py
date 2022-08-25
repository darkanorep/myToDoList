from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, session, jsonify
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
            flash("This username was already taken.", category='error')
        
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



@auth.route("/mytodolist", methods=['GET', 'POST'])
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

        todoArray = []

        for row in todo:

            todo_id = row['todo_id']
            # action = -1

            cur.execute("SELECT type FROM ToDo WHERE todo_id=? AND username=?", [todo_id, username])
            type = cur.fetchone()
            # not_done = not_done['not_done']


            todoObjects = {
                'todo_id': row['todo_id'],
                'todo_name': row['todo_name'],
                'type': type['type']
            }

            todoArray.append(todoObjects)

            dtodos = jsonify(todoArray)   

        return render_template('dashboard.html', user=user, todo=todo)
    
    else:
        return redirect(url_for("auth.login"))


@auth.route('/done-undone', methods=['POST', 'GET'])
def doneundone():

    if "user" in session:

        con  = myDb()
        con.row_factory = sqlite3.Row  
        cur = con.cursor()

        username = session["user"]
    
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

            # time_format = "%B %d, %Y %I:%M%p"
            # now = datetime.now().strftime(time_format)
            # tz = ['Asia/Manila']

            # for zone in tz:
            #     date = datetime.now(timezone(zone)).strftime(time_format)

            cur.execute("INSERT into ToDo (todo_name, username, type) values (?,?,?)",(todoName, username, 0))
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


@auth.route('/update_todo/<id>', methods=["POST","GET"])
def updateToDo(id):

    if "user" in session:

        con  = myDb()
        con.row_factory = sqlite3.Row  
        cur = con.cursor()

        cur.execute("SELECT * FROM ToDo where todo_id=?",([id]))
        data = cur.fetchone()

        if request.method == 'POST':
            name = request.form['name']

            if data:
                cur.execute("UPDATE ToDO SET todo_name=? where todo_id=?",(name,id))
                con.commit()

                flash("Successfully Updated", category="success")

                return redirect(url_for("auth.myToDoList"))
            
            else:
                flash("Update Failed", category="error")

        return render_template('update_todo.html', data=data)
    
    else:
        return redirect(url_for("auth.login"))


@auth.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for('auth.login'))
