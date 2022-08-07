from todowebapp import create_app
from flask import Flask, render_template


app = Flask(__name__)
app = create_app()

@app.route("/")
def index():

    return render_template("base.html")
    


if __name__ == '__main__':
   app.run(debug = True)