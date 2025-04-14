from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="hospital_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pw))
        result = cursor.fetchone()
        if result:
            session['username'] = user
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', user=session['username'])
    return redirect(url_for('login'))

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        cursor.execute("INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)",
                       (name, age, gender, disease))
        db.commit()

        return "Patient added successfully! <a href='/dashboard'>Back to Dashboard</a>"

    return render_template('add_patient.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        date = request.form['appointment_date']

        cursor.execute("INSERT INTO appointments (patient_name, doctor_name, appointment_date) VALUES (%s, %s, %s)",
                       (patient_name, doctor_name, date))
        db.commit()

        return "Appointment booked successfully! <a href='/dashboard'>Back</a>"

    return render_template('appointments.html')

@app.route('/patient_records', methods=['GET', 'POST'])
def patient_records():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        treatment_details = request.form['treatment_details']
        bill_amount = request.form['bill_amount']

        cursor.execute("INSERT INTO patient_records (patient_name, treatment_details, bill_amount) VALUES (%s, %s, %s)",
                       (patient_name, treatment_details, bill_amount))
        db.commit()

        return "Record saved! <a href='/dashboard'>Back</a>"

    return render_template('patient_records.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
