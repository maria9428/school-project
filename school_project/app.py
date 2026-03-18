from flask import Flask, render_template, request, redirect, session, url_for
import pymysql

app= Flask(__name__)
app.secret_key="schoolsecret"

db=pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="Abc@12345",
    database="school"
    )

cursor=db.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name=request.form["name"]
    student_class=request.form["class"]
    roll=request.form["roll"]

    sql="insert into student (name,class,roll) VALUES (%s,%s,%s)"
    values=(name,student_class,roll)

    cursor.execute(sql, values)
    db.commit()
    return "Student saved in database!"

@app.route("/students")
def students():
    if 'user' not in session:
        return redirect("/login")
    query=request.args.get("q")

    if query:
        sql="select * from student where name like %s or class like %s or roll like %s"
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
    sql = "DELETE FROM student WHERE id=%s"
    cursor.execute(sql, (id,))
    db.commit()
    return redirect("/students")

@app.route("/edit/<int:id>")
def edit(id):
    if 'user' not in session:
        return redirect("/login")
    cursor.execute("SELECT * FROM student WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template("edit.html", student=student)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if 'user' not in session:
        return redirect("/login")
    name = request.form['name']
    class_name = request.form['class']
    roll = request.form['roll']

    sql = "UPDATE student SET name=%s, class=%s, roll=%s WHERE id=%s"
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
    
