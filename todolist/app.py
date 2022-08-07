from todowebapp import create_app
from flask import Flask, render_template, request, flash
import sqlite3


app = Flask(__name__)
app = create_app()

# con = sqlite3.connect("todo.db")  
# print("Database opened successfully")  
# con.execute("create table User (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT  UNIQUE NOT NULL, password TEXT NOT NULL, confirmPassword TEXT NOT NULL)")  
# print("Table created successfully")  

# con = sqlite3.connect('todo.db')  
# con.row_factory = sqlite3.Row  
# cur = con.cursor()

@app.route("/")
def index():

    return render_template("index.html")
    
@app.route("/signup", methods=['POST','GET'])
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
            flash("This email was already taken.", category='e')
        
        else:
            cur.execute("INSERT into User (username, password, confirmPassword) values (?,?,?)",(username, password, confirmPassword))
            con.commit()

            flash("Successfully registered.", category='s')

    return render_template("signup.html")

if __name__ == '__main__':
   app.run(debug = True)