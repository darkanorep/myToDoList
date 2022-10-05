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

def time():

    time_format = '%B %d, %Y %H:%M:%S.%f'[:-3]
    now = datetime.now().strftime(time_format)
    tz = ['Asia/Manila']

    for zone in tz:
        date = datetime.now(timezone(zone)).strftime(time_format)
    
    return date

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
        
        elif (password != confirmPassword):
            flash("Password does not match.", category='error')
        
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

        cur.execute("SELECT * FROM ToDO where username=? and type='0' ORDER BY date desc",([username]))
        todo = cur.fetchall()

        cur.execute("SELECT * FROM ToDO where username=? and type='1' ORDER BY date desc",([username]))
        done = cur.fetchall()


        return render_template('dashboard.html', user=user, todo=todo, done=done)
    
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
            date = time()

            cur.execute("INSERT into ToDo (todo_name, username, date, type) values (?,?,?,?)",(todoName, username, date, 0))
            con.commit()

            flash("Successfully Added!",category='success')
            
            return redirect(url_for('auth.myToDoList'))

        return render_template("dashboard.html")
    
    else:
        return redirect(url_for("auth.login"))

@auth.route("/delete-todo/<id>")
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

@auth.route("/done-todo/<id>")
def doneToDo(id):

    if "user" in session:

        try:
            con  = myDb()
            con.row_factory = sqlite3.Row  
            cur = con.cursor()
            date = time()

            cur.execute("UPDATE ToDO SET type='1' where todo_id=?",([id]))
            con.commit()

            flash("Congrats!!",category='success')

        except:
            flash("Record Delete Failed","danger",category="error")

        finally:
            return redirect(url_for("auth.myToDoList"))
    
    else:
        return redirect(url_for("auth.login"))

@auth.route("/undone-todo/<id>")
def undoneToDo(id):

    if "user" in session:

        try:
            con  = myDb()
            con.row_factory = sqlite3.Row  
            cur = con.cursor()

            cur.execute("UPDATE ToDO SET type='0' where todo_id=?",([id]))
            con.commit()

            flash("Successfully Undone!!",category='success')

        except:
            flash("Record Delete Failed","danger",category="error")

        finally:
            return redirect(url_for("auth.myToDoList"))
    
    else:
        return redirect(url_for("auth.login"))

@auth.route("/delete-done/<id>")
def deleteDone(id):

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
