from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['CSF']  # Replace 'CSF' with your actual database name
collection = db['details']  # Replace 'details' with your actual collection name

# Dictionary of teacher credentials (replace with database lookup)
teacher_credentials = {
    'teacher1': 'password1',
    'teacher2': 'password2'
}

@app.route('/')
def index():
    # Check if teacher is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        # Retrieve student data from MongoDB
        students = list(collection.find({}, {'_id': 0, 'name': 1, 'enrollment_no': 1}))  # Only include 'name' and 'enrollment_no' fields
        return render_template('index.html', students=students)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if credentials are valid
        if username in teacher_credentials and teacher_credentials[username] == password:
            # Start session and redirect to index page
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear session data and redirect to login page
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    if request.method == 'POST':
        # Check if teacher is logged in
        if 'username' not in session:
            return redirect(url_for('login'))

        # Get attendance data from the form
        attendance_data = {}
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                index = int(key.split('_')[-1])
                attendance_data[index] = value

        # Update attendance in MongoDB
        for index, attendance in attendance_data.items():
            # Assuming 'attendance' field doesn't exist in the original document
            collection.update_one({'name': request.form['name_' + str(index)]}, {'$set': {'attendance': attendance}})

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
