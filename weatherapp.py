from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="popcorns",
        database="weatherapp"
    )

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = None

        try:
            db = connect_to_database()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                # Store user ID in session
                session['user_id'] = user[0]  # Assuming user[0] is the ID
                return redirect(url_for('weather_data'))
            else:
                flash('Invalid username or password', 'error')
        except mysql.connector.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            if db is not None:
                db.close()

    return render_template('login.html')

# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = None

        try:
            db = connect_to_database()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            flash('User created successfully', 'success')
        except mysql.connector.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            if db is not None:
                db.close()
    return render_template('signup.html')

# Weather data route
@app.route('/weather')
def weather_data():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))

    db = None
    try:
        db = connect_to_database()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM weather_data WHERE user_id=%s ORDER BY recorded_at DESC LIMIT 1", (user_id,))
        data = cursor.fetchone()
        if data:
            recorded_at = data[1]  # Timestamp
            temperature = data[2]   # Temperature
            humidity = data[3]      # Humidity
            moisture = data[4]      # Moisture
            return render_template('weather.html', 
                                   recorded_at=recorded_at, 
                                   temperature=temperature, 
                                   humidity=humidity, 
                                   moisture=moisture)
        else:
            flash('No weather data available for you.', 'info')
            return render_template('weather.html', recorded_at=None)
    except mysql.connector.Error as e:
        flash(f"Database error: {e}", 'error')
        return redirect(url_for('login'))
    finally:
        if db is not None:
            db.close()


if __name__ == '__main__':
    app.run(debug=True)
