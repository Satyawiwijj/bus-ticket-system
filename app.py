from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='yourpassword',
    database='bus_system'
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()
    return render_template('index.html', buses=buses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM bookings WHERE user_id=%s", (session['user_id'],))
    bookings = cursor.fetchall()
    return render_template('dashboard.html', bookings=bookings)

@app.route('/book/<int:bus_id>')
def book(bus_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor.execute("INSERT INTO bookings (user_id, bus_id) VALUES (%s, %s)", (session['user_id'], bus_id))
    conn.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        route = request.form['route']
        time = request.form['time']
        seats = request.form['seats']
        cursor.execute("INSERT INTO buses (route, time, seats) VALUES (%s, %s, %s)", (route, time, seats))
        conn.commit()
    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()
    return render_template('admin.html', buses=buses)

if __name__ == '__main__':
    app.run(debug=True)
