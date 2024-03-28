from flask import render_template
from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
username = 'root'
password = 'password'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
server   = 'localhost'
dbname   = '/clinicproject'

# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning
db = SQLAlchemy(app)

class PatientInformation(db.Model):
    __tablename__ = 'Patient_Information'
    Patient_ID = db.Column(db.Integer, primary_key=True)
    Height = db.Column(db.Integer)
    Weight = db.Column(db.Integer)
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(50))
    Blood_Pressure = db.Column(db.Integer)
    Medication = db.Column(db.Text)
    Symptoms = db.Column(db.Text)
    Reason_for_visit = db.Column(db.Text)
    Last_Reason_for_visit = db.Column(db.Text)
    Doctor_in_care = db.Column(db.Integer, db.ForeignKey('Employee.Employee_ID'))
    
    # Assuming a one-to-one relationship with Nurse_Form
    nurse_form = db.relationship('NurseForm', backref='patient_information', uselist=False)

class NurseForm(db.Model):
    __tablename__ = 'Nurse_Form'
    Patient_ID = db.Column(db.Integer, db.ForeignKey('Patient_Information.Patient_ID'), primary_key=True)
    Height = db.Column(db.Integer)
    Weight = db.Column(db.Integer)
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(50))
    Blood_Pressure = db.Column(db.Integer)
    Medication = db.Column(db.Text)
    Symptoms = db.Column(db.Text)
    Doctor_in_care = db.Column(db.Integer)

class Insurance(db.Model):
    __tablename__ = 'Insurance'
    Insurance_Name = db.Column(db.Integer, primary_key=True)
    Policy_Number = db.Column(db.Integer)
    Covered = db.Column(db.Boolean)
    Deductible = db.Column(db.Integer)
    
    # Assuming a one-to-many relationship with Patient
    patients = db.relationship('Patient', backref='insurance')

class Patient(db.Model):
    __tablename__ = 'Patient'
    Patient_ID = db.Column(db.Integer, db.ForeignKey('Patient_Information.Patient_ID'), primary_key=True)
    FName = db.Column(db.String(50))
    LName = db.Column(db.String(50))
    Insurance_Name = db.Column(db.Integer, db.ForeignKey('Insurance.Insurance_Name'))
    Covered = db.Column(db.Boolean)
    Phone = db.Column(db.Integer)
    Address = db.Column(db.String(255))
    EContact_Name = db.Column(db.String(50))
    EContact_Phone = db.Column(db.Integer)

class Employee(db.Model):
    __tablename__ = 'Employee'
    Employee_ID = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.String(50))
    FName = db.Column(db.String(50))
    LName = db.Column(db.String(50))
    HiredDate = db.Column(db.Date)
    PTO = db.Column(db.Integer)
    Sick_Days = db.Column(db.Integer)
    
    # Relationships with PatientInformation and Employee_schedule
    patients_in_care = db.relationship('PatientInformation', backref='doctor')
    schedules = db.relationship('EmployeeSchedule', backref='employee')

class EmployeeSchedule(db.Model):
    __tablename__ = 'Employee_schedule'
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employee.Employee_ID'), primary_key=True)
    Date = db.Column(db.Date, primary_key=True)
    Time = db.Column(db.Time, primary_key=True)

class Schedule(db.Model):
    __tablename__ = 'Schedule'
    Patient_ID = db.Column(db.Integer, db.ForeignKey('Patient.Patient_ID'), primary_key=True)
    Employee_ID = db.Column(db.Integer, db.ForeignKey('Employee.Employee_ID'), primary_key=True)
    Date = db.Column(db.Date, primary_key=True)
    Time = db.Column(db.Time, primary_key=True)
    Type_of_visit = db.Column(db.String(50))

class User_Account(db.Model):
    __tablename__ = 'User_Account'
    User_ID = db.Column(db.Integer,primary_key=True)
    Patient_ID = db.Column(db.Integer)
    Username = db.Column(db.String(50))
    Password_Hash = db.Column(db.String(60))


@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        # Assuming you're sending data via a form and using Flask's request to access it
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        # Create an instance of the Patient
        new_patient = Patient(FName=fname, LName=lname)
        # Add to the session and commit to the database
        db.session.add(new_patient)
        db.session.commit()
        return jsonify(message='Patient added successfully'), 201



@app.route('/delete_patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    # Query for the specific patient
    patient_to_delete = Patient.query.get(patient_id)
    if patient_to_delete:
        db.session.delete(patient_to_delete)
        db.session.commit()
        return jsonify(message='Patient deleted successfully'), 200
    else:
        return jsonify(error='Patient not found'), 404



@app.route('/edit_patient/<int:patient_id>', methods=['PUT'])
def edit_patient(patient_id):
    # Query for the specific patient
    patient = Patient.query.get(patient_id)
    if patient:
        patient.FName = request.form.get('fname', patient.FName)
        patient.LName = request.form.get('lname', patient.LName)
        # Add other fields as necessary
        db.session.commit()
        return jsonify(message='Patient updated successfully'), 200
    else:
        return jsonify(error='Patient not found'), 404


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/pay')
def pay():
    return render_template('pay.html')

@app.route('/appt')
def appt():
    return render_template('appt.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
