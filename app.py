from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = '123!"£Qwe'  # Replace with a strong secret key

# Create a SQLite database and tables for user registration data and reviews
db = sqlite3.connect('users.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        username TEXT,
        review_text TEXT
    )
''')
db.commit()
db.close()

@app.route('/')
def index():
    if 'username' in session:
        location_confirmation = session.get('location')
        return render_template('directions.html', location_confirmation=location_confirmation)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        # Check if the username already exists in the database
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            db.close()
            return 'Username already exists. Please choose another username.'

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        db.commit()
        db.close()

        return redirect(url_for('registration_success'))

    return render_template('register.html')

@app.route('/registration_success')
def registration_success():
    return 'Registration successful! You can now <a href="/login">log in</a>.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        # Check if the username and password match in the database
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        authenticated_user = cursor.fetchone()
        db.close()

        if authenticated_user:
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))

        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

@app.route('/view_reviews')
def view_reviews():
    db = sqlite3.connect('users.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM reviews')
    reviews = cursor.fetchall()
    db.close()
    return render_template('view_reviews.html', reviews=reviews)

@app.route('/leave_review', methods=['GET', 'POST'])
def leave_review():
    if request.method == 'POST':
        review_text = request.form['review_text']
        username = session['username']

        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        # Insert the new review into the database
        cursor.execute('INSERT INTO reviews (username, review_text) VALUES (?, ?)', (username, review_text))
        db.commit()
        db.close()

        return 'Review submitted successfully'

    return render_template('leave_review.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/confirm_location', methods=['POST'])
def confirm_location():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        session['location'] = {'latitude': latitude, 'longitude': longitude}
        return render_template('map.html', location_confirmation=session['location'])

if __name__ == '__main__':
    app.run(debug=True)
