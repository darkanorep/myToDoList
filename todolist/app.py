from todowebapp import create_app
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
app = create_app()


# print("Database opened successfully")  
# con.execute("create table User (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT  UNIQUE NOT NULL, password TEXT NOT NULL, confirmPassword TEXT NOT NULL)")  
# # print("Table created successfully")  
# con = sqlite3.connect('todo.db')  
# con.row_factory = sqlite3.Row  
# cur = con.cursor()
# con.execute("create table ToDo (todo_id INTEGER PRIMARY KEY AUTOINCREMENT, todo_name TEXT NOT NULL, date DATE NOT NULL)")

@app.route("/")
def index():

    return render_template("index.html")


if __name__ == '__main__':
   app.run(debug = True)