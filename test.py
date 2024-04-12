import flask
from flask import Flask, redirect, url_for, render_template, jsonify,request
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
import flask_login
users = {'foo@bar.tld': {'password': 'secret'}} # temp for login testing

#controls which database to use
use_local_db = False

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!
#modify theses to match the database you want to test
#!@QWASZX12qwaszx my azure database password
username = 'root'
password = ''
server   = 'localhost'
dbname   = 'testdb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + username + ':' + password + '@' + server + dbname 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to suppress a warning

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
db = SQLAlchemy(app)

# Load the test.sql schema to your DB before testing
class User(db.Model):
    __tablename__ = 'users'
    ID = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String(255))
    lname = db.Column(db.String(255))

    def __init__(self, first, last):
        self.fname = first
        self.lname = last

    def __str__(self):
        return f"<first={self.fname}, last={self.lname}>"
    
""" class Insurance(db.Model):
    __tablename__ = 'insurance'
    ID = db.Column(db.Integer,primary_key=True)
    Insurance_Name = db.Column(db.String(255))
    Policy_Number = db.Column(db.Integer)
    Deductible = db.column(db.Integer, nullable = False)

class Patient(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    Fname = db.Column(db.String(255), nullable = False)
    Lname = db.Column(db.String(255), nullable = False)
    Has_Insurance = db.column(db.Boolean, nullable = False)
    # add insurance as foriegn key
    Insurance_Name = db.Column(db.String(255))
    Phone = db.column(db.Integer)
    Address = db.column(db.String(255))
    EContanct_Name = db.column(db.String(255))
    EContact_Phone = db.column(db.Integer)

class Employee(db.Model):
    ID = db.Column(db.Integer,primary_key=True)
    Position = db.column(db.String(255), nullable = False)
    Fname = db.Column(db.String(255), nullable = False)
    Lname = db.Column(db.String(255), nullable = False)
    HiredDate = db.column(db.DateTime, nullable = False)
    PTO = db.column(db.Integer)
    Sick_Days = db.column(db.Integer)

class PatientInformation(db.Model):
    # foreign key for patient
    ID = db.Column(db.Integer,primary_key=True)
    Height = db.column(db.Integer)
    Weight = db.column(db.Float)
    Age = db.column()
    Sex  = db.column()
    Blood_Pressure = db.column()
    Medication = db.column()
    Symptoms = db.column()
    Reason_For_Visit = db.column()
    Last_Reason_For_Visit = db.column()
    Doctor_In_Care = db.column()

class EmployeeSchedule(db.Model):
    ID = db.column(db.Integer, primary_key = True)
    Date = db.column()
    Time = db.column()

class AppointmentSchedule(db.Model):
    Patient_ID = db.column()
    Doctor_ID = db.column()
    Nurse_ID = db.column()
    Date = db.column()
    Time = db.column()
    Type_of_Visit = db.column()
 """

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user
    
@app.route("/")
def test():
    return render_template('test.html')

# User Login Views
@app.route("/testsubmit", methods=['GET','POST'])
def testsubmit():
    if request.method == 'POST':
        first = request.form.get("fname")
        last = request.form.get("lname")
        user = User(first, last)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("testusers"))
        except Exception as e:
            return jsonify(error=str(e))
    #redirect on a GET request
    return redirect(url_for("testusers"))
    
@app.route("/testusers", methods=['GET'])
def testusers():
    result = User.query.all()
    return render_template("/testusers.html", results = result )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = flask.request.form['email']
    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401