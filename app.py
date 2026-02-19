from flask import Flask, render_template, request, redirect, session
import sqlite3  # SQLite module for database operations

# ------------------------------
# Flask App Initialization
# ------------------------------
app = Flask(__name__)
app.secret_key = "secret123"  # Secret key for session management (required for sessions)

# ------------------------------
# Database Connection Function
# ------------------------------
def db_connection():
    """
    Returns a connection object to the SQLite database.
    database.db is a binary SQLite file; do NOT open it in VS Code editor.
    Use this function to interact with the database in Python.
    """
    return sqlite3.connect("database.db")

# ------------------------------
# Create Tables if They Do Not Exist
# ------------------------------
with db_connection() as conn:
    # Users table: stores registered users
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    # Students table: stores student info
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        grade TEXT
    )
    """)

    # Courses table: stores course info
    conn.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        teacher TEXT
    )
    """)

    # Assignments table: stores assignment info
    conn.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

# ------------------------------
# Authentication Routes
# ------------------------------
@app.route("/")
def login():
    """Display login page."""
    return render_template("login.html")

@app.route("/signup")
def signup():
    """Display signup page."""
    return render_template("signup.html")

@app.route("/register", methods=["POST"])
def register():
    """Handle new user registration."""
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    with db_connection() as conn:
        # Insert new user into database
        conn.execute("INSERT INTO users VALUES (NULL,?,?,?)", (name, email, password))
    
    # Redirect to login page after registration
    return redirect("/")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    """Handle user login."""
    email = request.form["email"]
    password = request.form["password"]

    with db_connection() as conn:
        # Check if user exists with provided email and password
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?", (email, password)
        ).fetchone()

    if user:
        session["user"] = user[1]  # Save username in session
        return redirect("/dashboard")
    
    # Redirect to login if authentication fails
    return redirect("/")

@app.route("/logout")
def logout():
    """Logout user by clearing session."""
    session.clear()
    return redirect("/")

# ------------------------------
# Dashboard Route
# ------------------------------
@app.route("/dashboard")
def dashboard():
    """Display the main dashboard with statistics."""
    if "user" not in session:
        return redirect("/")

    with db_connection() as conn:
        # Fetch all students, courses, and assignments
        students = conn.execute("SELECT * FROM students").fetchall()
        courses = conn.execute("SELECT * FROM courses").fetchall()
        assignments = conn.execute("SELECT * FROM assignments").fetchall()
    
    # Calculate basic statistics
    stats = {
        "total_students": len(students),
        "total_courses": len(courses),
        "pending_assignments": len([a for a in assignments if str(a[3]).lower() == 'pending']),
        "grades_count": {}
    }

    for s in students:
        grade = s[3]
        stats["grades_count"][grade] = stats["grades_count"].get(grade, 0) + 1

    # Render dashboard template with data
    return render_template(
        "dashboard.html",
        students=students,
        courses=courses,
        assignments=assignments,
        stats=stats
    )

# ------------------------------
# Student CRUD
# ------------------------------
@app.route("/add_student", methods=["POST"])
def add_student():
    """Add a new student."""
    name = request.form["name"]
    age = request.form["age"]
    grade = request.form["grade"]

    with db_connection() as conn:
        conn.execute("INSERT INTO students VALUES (NULL,?,?,?)", (name, age, grade))
    
    # Redirect to /students if coming from that page, else dashboard
    referrer = request.referrer
    if referrer and '/students' in referrer:
        return redirect("/students")
    return redirect("/dashboard")

@app.route("/students")
def students():
    """List all students."""
    if "user" not in session:
        return redirect("/")
    
    with db_connection() as conn:
        students_list = conn.execute("SELECT * FROM students").fetchall()
    
    stats = {"total_students": len(students_list), "grades_count": {}}
    for s in students_list:
        stats["grades_count"][s[3]] = stats["grades_count"].get(s[3], 0) + 1

    return render_template("students.html", students=students_list, stats=stats)

@app.route("/edit_student/<int:id>")
def edit_student(id):
    """Display edit page for a specific student."""
    if "user" not in session:
        return redirect("/")
    
    with db_connection() as conn:
        student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    
    if not student:
        return redirect("/students")
    
    return render_template("edit_student.html", student=student)

@app.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):
    """Update student information."""
    name = request.form["name"]
    age = request.form["age"]
    grade = request.form["grade"]

    with db_connection() as conn:
        conn.execute("UPDATE students SET name=?, age=?, grade=? WHERE id=?", (name, age, grade, id))
    
    return redirect("/students")

@app.route("/delete_student/<int:id>")
def delete_student(id):
    """Delete a student."""
    with db_connection() as conn:
        conn.execute("DELETE FROM students WHERE id=?", (id,))
    return redirect("/students")

# ------------------------------
# Course CRUD
# ------------------------------
@app.route("/add_course", methods=["POST"])
def add_course():
    """Add a new course."""
    name = request.form["course_name"]
    teacher = request.form["teacher"]
    with db_connection() as conn:
        conn.execute("INSERT INTO courses VALUES (NULL,?,?)", (name, teacher))
    
    referrer = request.referrer
    if referrer and '/courses' in referrer:
        return redirect("/courses")
    return redirect("/dashboard")

@app.route("/courses")
def courses():
    """List all courses."""
    if "user" not in session:
        return redirect("/")
    
    with db_connection() as conn:
        courses_list = conn.execute("SELECT * FROM courses").fetchall()
    
    stats = {"total_courses": len(courses_list)}
    return render_template("courses.html", courses=courses_list, stats=stats)

@app.route("/edit_course/<int:id>")
def edit_course(id):
    """Display edit page for a course."""
    if "user" not in session:
        return redirect("/")
    
    with db_connection() as conn:
        course = conn.execute("SELECT * FROM courses WHERE id=?", (id,)).fetchone()
    
    if not course:
        return redirect("/courses")
    
    return render_template("edit_course.html", course=course)

@app.route("/update_course/<int:id>", methods=["POST"])
def update_course(id):
    """Update course info."""
    course_name = request.form["course_name"]
    teacher = request.form["teacher"]
    with db_connection() as conn:
        conn.execute("UPDATE courses SET course_name=?, teacher=? WHERE id=?", (course_name, teacher, id))
    return redirect("/courses")

@app.route("/delete_course/<int:id>")
def delete_course(id):
    """Delete a course."""
    with db_connection() as conn:
        conn.execute("DELETE FROM courses WHERE id=?", (id,))
    return redirect("/courses")

# ------------------------------
# Assignment CRUD
# ------------------------------
@app.route("/add_assignment", methods=["POST"])
def add_assignment():
    """Add a new assignment."""
    title = request.form["title"]
    due_date = request.form["due_date"]
    status = request.form.get("status", "Pending")
    
    with db_connection() as conn:
        conn.execute("INSERT INTO assignments (title, due_date, status) VALUES (?,?,?)", (title, due_date, status))
    
    referrer = request.referrer
    if referrer and '/assignments' in referrer:
        return redirect("/assignments")
    return redirect("/dashboard")

@app.route("/assignments")
def assignments():
    """List all assignments with stats."""
    if "user" not in session:
        return redirect("/")
    
    with db_connection() as conn:
        assignments_list = conn.execute("SELECT * FROM assignments").fetchall()
    
    stats = {
        "total_assignments": len(assignments_list),
        "pending_assignments": len([a for a in assignments_list if str(a[3]).lower() == 'pending']),
        "completed_assignments": len([a for a in assignments_list if str(a[3]).lower() == 'completed'])
    }
    
    return render_template("assignments.html", assignments=assignments_list, stats=stats)

@app.route("/edit_assignment/<int:id>")
def edit_assignment(id):
    """Display edit page for an assignment."""
    if "user" not in session:
        return redirect("/")
    
    with db_connection() as conn:
        assignment = conn.execute("SELECT * FROM assignments WHERE id=?", (id,)).fetchone()
    
    if not assignment:
        return redirect("/assignments")
    
    return render_template("edit_assignment.html", assignment=assignment)

@app.route("/update_assignment/<int:id>", methods=["POST"])
def update_assignment(id):
    """Update assignment info."""
    title = request.form["title"]
    due_date = request.form["due_date"]
    status = request.form["status"]
    with db_connection() as conn:
        conn.execute("UPDATE assignments SET title=?, due_date=?, status=? WHERE id=?", (title, due_date, status, id))
    return redirect("/assignments")

@app.route("/delete_assignment/<int:id>")
def delete_assignment(id):
    """Delete an assignment."""
    with db_connection() as conn:
        conn.execute("DELETE FROM assignments WHERE id=?", (id,))
    return redirect("/assignments")

# ------------------------------
# Run Flask App
# ------------------------------
if __name__ == "__main__":
    # Debug mode = True allows automatic reloads and detailed error messages
    app.run(debug=True)
