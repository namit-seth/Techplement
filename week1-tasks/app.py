from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required , apology
import mysql.connector

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="TODO"
)
cur = con.cursor()

@app.route("/")
@login_required
def index():
    cur.execute("select * from task where user_id = %s",(session["user_id"],))
    tasks = cur.fetchall()
    return render_template("index.html", tasks = tasks)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method != "POST":
        return render_template("login.html")
    if not request.form.get("id"):
        return apology("must provide username")
    if not request.form.get("password"):
        return apology("must provide password")
    
    username = request.form.get("id")
    password = request.form.get("password")

    cur.execute("select * from user where username = %s",(username,))
    rows = cur.fetchall()
    con.commit()
    if len(rows) != 1 :
        return apology("Invalid username")
    if not check_password_hash(rows[0][2] , password):
        return apology("incorrect password")
    session["user_id"] = rows[0][0]
    print("logged in")
    return redirect("/")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method != "POST":
        return render_template("signup.html")
    
    if not request.form.get("id"):
        return apology("must provide username")
    if not request.form.get("password"):
        return apology("must provide password")
    if not request.form.get("cnfrm_pass"):
        return apology("must provide confirm password")
    
    username = request.form.get("id")
    password = request.form.get("password")
    cnfrm_pass = request.form.get("cnfrm_pass")

    if password != cnfrm_pass:
        return apology("password and confirm password are not same")
    
    cur.execute(
        "INSERT INTO user (username, password) VALUES (%s, %s)",
        (username , generate_password_hash(password))
    )
    con.commit()
    print("sign_up")
    return redirect("/login")

@app.route("/logout/")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/add", methods=["POST" , ] )
@login_required
def add():
    task = request.form.get("task")
    cur.execute(
        "INSERT INTO task (user_id, task) VALUES (%s, %s)",
        (session["user_id"] , task)
    )
    con.commit()
    return redirect("/")

@app.route("/del", methods=["POST" , ] )
@login_required
def delete():
    id = request.form.get("id")
    cur.execute(
        "DELETE FROM task WHERE id = %s",
        (id , )
    )
    con.commit()
    return redirect("/")

@app.route("/edit", methods=["POST" , ] )
@login_required
def edit():
    id = request.form.get("id")
    task = str(request.form.get("task"))
    cur.execute(
        "UPDATE task SET task = %s WHERE id = %s",
        (task , id )
    )
    con.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000, debug=True)