# Student Management System

A Flask-based web application for managing students, courses, and assignments. This system allows users to register, authenticate, and manage educational resources through an intuitive dashboard.

## Features

- **User Authentication**: User registration and login system
- **Student Management**: Add, view, edit, and delete student records
- **Course Management**: Manage courses and their instructors
- **Assignment Management**: Track assignments and their status
- **Dashboard**: Overview of all students, courses, and assignments with statistics
- **Database**: SQLite database for persistent data storage

## Project Structure

```
.
├── app.py                 # Main Flask application
├── database.db            # SQLite database (auto-created)
├── requirements.txt       # Python dependencies
├── static/
│   └── style.css         # CSS styling for the application
└── templates/
    ├── login.html        # User login page
    ├── signup.html       # User registration page
    ├── dashboard.html    # Main dashboard view
    ├── students.html     # Students management page
    ├── courses.html      # Courses management page
    ├── assignments.html  # Assignments management page
    ├── edit_student.html # Student edit form
    ├── edit_course.html  # Course edit form
    └── edit_assignment.html # Assignment edit form
```

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd studentt
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install flask
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Usage

### Getting Started

1. **Register a New Account**:
   - Click on "Sign Up" on the login page
   - Enter your name, email, and password
   - Click "Register"

2. **Login**:
   - Enter your email and password
   - Click "Login"

3. **Dashboard**:
   - View overview statistics
   - See all students, courses, and assignments
   - Quick access to management pages

### Managing Students

- **View Students**: Go to the Students section
- **Add Student**: Click "Add New Student" and fill in details
- **Edit Student**: Click the edit icon next to a student
- **Delete Student**: Click the delete button

### Managing Courses

- **View Courses**: Go to the Courses section
- **Add Course**: Click "Add New Course"
- **Edit Course**: Click the edit icon next to a course
- **Delete Course**: Click the delete button

### Managing Assignments

- **View Assignments**: Go to the Assignments section
- **Add Assignment**: Click "Add New Assignment"
- **Edit Assignment**: Click the edit icon next to an assignment
- **Change Status**: Update assignment status (Pending/Completed)

## Database Schema

### Users Table
```
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- email (TEXT)
- password (TEXT)
```

### Students Table
```
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- age (INTEGER)
- grade (TEXT)
```

### Courses Table
```
- id (INTEGER, PRIMARY KEY)
- course_name (TEXT)
- teacher (TEXT)
```

### Assignments Table
```
- id (INTEGER, PRIMARY KEY)
- title (TEXT)
- due_date (TEXT)
- status (TEXT, DEFAULT: 'Pending')
```

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS
- **Session Management**: Flask Sessions

## Security Notes

⚠️ **Important**: This application is for educational purposes. For production use:
- Use hashed passwords (e.g., `werkzeug.security`)
- Implement proper authentication and authorization
- Use environment variables for secret keys
- Add CSRF protection
- Validate and sanitize all user inputs
- Use HTTPS/SSL

## Configuration

### Secret Key
The application uses a simple secret key: `secret123`

To change it, modify line 6 in `app.py`:
```python
app.secret_key = "your_secure_key_here"
```

## Troubleshooting

- **Database errors**: Delete `database.db` to reset the database
- **Port already in use**: Modify the port in `app.py` or stop other services
- **Module not found**: Ensure Flask is installed: `pip install flask`

## Future Enhancements

- User roles and permissions
- Email notifications
- Grade tracking
- File uploads for assignments
- API endpoints
- Search and filter functionality
- Dark mode theme

## License

This project is open source and available for educational use.

## Support

For issues or questions, please check the code comments or review the Flask documentation at https://flask.palletsprojects.com/
