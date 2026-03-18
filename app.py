from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app= Flask(__name__)
app.secret_key="schoolsecret"

db = sqlite3.connect("school.db", check_same_thread=False)
cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    class TEXT,
    roll TEXT
)
""")
db.commit()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name=request.form["name"]
    student_class=request.form["class"]
    roll=request.form["roll"]
    sql = "INSERT INTO student (name, class, roll) VALUES (?, ?, ?)"
    cursor.execute(sql, (name, class_name, roll))
    db.commit()
    return "Student saved in database!"

@app.route("/students")
def students():
    if 'user' not in session:
        return redirect("/login")
    query=request.args.get("q")

    if query:
        sql="select * from student where name like ? or class like ? or roll like ?"
        cursor.execute(sql,('%'+query+'%','%'+query+'%','%'+query+'%'))
    else:
        cursor.execute("select * from student")
    
    data=cursor.fetchall()
    return render_template("students.html",students=data)

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/delete/<int:id>")
def delete(id):
    if 'user' not in session:
        return redirect("/login")
    sql = "DELETE FROM student WHERE id=?"
    cursor.execute(sql, (id,))
    db.commit()
    return redirect("/students")

@app.route("/edit/<int:id>")
def edit(id):
    if 'user' not in session:
        return redirect("/login")
    cursor.execute("SELECT * FROM student WHERE id=?", (id,))
    student = cursor.fetchone()
    return render_template("edit.html", student=student)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if 'user' not in session:
        return redirect("/login")
    name = request.form['name']
    class_name = request.form['class']
    roll = request.form['roll']

    sql = "UPDATE student SET name=?, class=?, roll=? WHERE id=?"
    cursor.execute(sql, (name, class_name, roll, id))
    db.commit()

    return redirect("/students")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect("/dashboard")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/login")

if __name__=="__main__":
    app.run(debug=True)
    
