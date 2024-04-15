from flask import request, jsonify, redirect, render_template, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
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
    insurance = StringField("Insurance Name:", validators=[DataRequired()])
    policy_num = IntegerField("Policy Number:", validators=[DataRequired()])
    phone = StringField("Phone Number:", validators=[DataRequired()])
    address = StringField("Address:", validators=[DataRequired()])
    econtact = StringField("Emergency Contact:", validators=[DataRequired()])
    econtact_phone = StringField("Emergency Contact Number:", validators=[DataRequired()])
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
    Doctor_in_care = db.Column(db.Integer)

class Patient(db.Model):
    __tablename__ = 'Patient'
    Patient_ID = db.Column(db.Integer, primary_key=True)
    FName = db.Column(db.String(50))
    LName = db.Column(db.String(50))
    Insurance_Name = db.Column(db.String(255))
    Policy_Number = db.Column(db.Integer)
    Covered = db.Column(db.Boolean)
    Phone = db.Column(db.String(15))
    Address = db.Column(db.String(255))
    EContact_Name = db.Column(db.String(50))
    EContact_Phone = db.Column(db.String(15))

    def __init__(self, fname, lname, insurance, policy_num, phone, address, econtact, econ_num):
        self.FName = fname
        self.LName = lname
        self.Insurance_Name = insurance
        self.Policy_Number = policy_num
        self.Phone = phone
        self.Address = address
        self.EContact_Name = econtact
        self.EContact_Phone = econ_num


class Employee(db.Model):
    __tablename__ = 'Employee'
    Employee_ID = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.String(50))
    FName = db.Column(db.String(50))
    LName = db.Column(db.String(50))
    HiredDate = db.Column(db.Date)
    PTO = db.Column(db.Integer)
    Sick_Days = db.Column(db.Integer)

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

with app.app_context():
    db.create_all()

@app.route("/")
def index():
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
    form = LoginForm()
    if form.validate_on_submit():
        #check if user exists with that email address
        user = User.query.filter_by(Email=form.email.data).first()
        if user:
            #check if password is correct
            if check_password_hash(user.Password_Hash, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            #redirect if password is incorrect
            else:
                print("incorrect password")
                return redirect(url_for("login"))
        #redirect if email not linked to account
        else:
            print("email not found")
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
    form = RegisterForm()
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        #check if user already exists
        user = User.query.filter_by(Email=form.email.data).first()
        if user is None:
            #add user to db
            hashed_pw = generate_password_hash(form.password.data)
            user = User(form.email.data, form.fname.data, form.lname.data, hashed_pw)
            db.session.add(user)
            patient = Patient(form.fname.data, 
                              form.lname.data, 
                              form.insurance.data, 
                              form.policy_num.data,
                              form.phone.data,
                              form.address.data,
                              form.econtact.data,
                              form.econtact_phone.data)
            db.session.add(patient)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        
    return render_template('register.html', form = form)

@app.route("/testusers", methods=['GET', 'POST'])
@login_required
def testusers():
    result = User.query.all()
    if result is None:
        return redirect(url_for("login"))
    return render_template("/testusers", results = result )

if __name__ == '__main__':
    app.run(debug=True)
