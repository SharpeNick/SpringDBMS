from flask import request, jsonify, redirect, render_template, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
username = 'root'
password = 'password123'
server   = 'localhost'
dbname   = '/clinicproject'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + username + ':' + password + '@' + server + dbname 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning
app.config['SECRET_KEY'] = "supersecretkey" #required for wtforms
db = SQLAlchemy(app)

# Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Forms
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    fname = StringField("First Name:", validators=[DataRequired()])
    lname = StringField("Last Name:", validators=[DataRequired()])
    email = StringField("Email Address:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

# DB Models
class User(db.Model, UserMixin):
    __tablename__ = 'User_Account'
    User_ID = db.Column(db.Integer,primary_key=True)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    FName = db.Column(db.String(50))
    LName = db.Column(db.String(50))
    Password_Hash = db.Column(db.String(255), nullable=False)
    Date_Added = db.Column(db.DateTime, default=datetime.now)

    def get_id(self):
        return self.User_ID
    
    def __init__(self, email, fname, lname, hashed_pw):
        self.Email = email
        self.FName = fname
        self.LName = lname
        self.Password_Hash = hashed_pw

    def __repr__(self):
        return '<Name %r>' % self.name

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

#with app.app_context():
    #db.create_all()

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    #validation
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user:
            if check_password_hash(user.Password_Hash, form.password.data):
                login_user(user)
                return redirect(url_for("hello_world"))
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))
        
    return render_template('login.html',
                           form = form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    email = None
    fname = None
    lname = None
    password = None
    confirm_password = None
    form = RegisterForm()
    
    if form.validate_on_submit():
        #check if user already exists
        user = User.query.filter_by(Email=form.email.data).first()
        if user is None:
            #add user to db
            hashed_pw = generate_password_hash(form.password.data)
            user = User(form.email.data, form.fname.data, form.lname.data, hashed_pw)
            db.session.add(user)
            db.session.commit()
    #clear form data
    email = form.email.data
    form.email.data = ''
    password = form.password.data
    form.password.data = ''
    confirm_password = form.confirm_password.data
    form.confirm_password.data = ''
    result = User.query.all()
    return render_template('register.html',
                           results = result,
                           email = email,
                           fname = fname,
                           lname = lname,
                           password = password,
                           confirm_password = confirm_password,
                           form = form)

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

@app.route("/testusers", methods=['GET', 'POST'])
@login_required
def testusers():
    result = User.query.all()
    if result is None:
        return redirect(url_for("login"))
    return render_template("/testusers", results = result )

if __name__ == '__main__':
    app.run(debug=True)
