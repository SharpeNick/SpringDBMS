from flask import request, jsonify, redirect, render_template, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Create_DB import createDatabase
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from Forms import RegisterAccountForm, RegisterPatientForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(SQLAlchemy.Model, UserMixin):
    __tablename__ = 'User_Account'
    User_ID = SQLAlchemy.Column(SQLAlchemy.Integer,primary_key=True)
    Email = SQLAlchemy.Column(SQLAlchemy.String(50), nullable=False, unique=True)
    FName = SQLAlchemy.Column(SQLAlchemy.String(50))
    LName = SQLAlchemy.Column(SQLAlchemy.String(50))
    Password_Hash = SQLAlchemy.Column(SQLAlchemy.String(255), nullable=False)
    Date_Added = SQLAlchemy.Column(SQLAlchemy.DateTime, default=datetime.now)
    Patient_ID = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey("Patient.Patient_ID"))

    def get_id(self):
        return self.User_ID
    
    def __init__(self, email, fname, lname, hashed_pw):
        self.Email = email
        self.FName = fname
        self.LName = lname
        self.Password_Hash = hashed_pw

    def __repr__(self):
        return '<Name %r>' % self.name

class PatientInformation(SQLAlchemy.Model):
    __tablename__ = 'Patient_Information'
    Patient_ID = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey('Patient.Patient_ID'),primary_key=True)
    Height = SQLAlchemy.Column(SQLAlchemy.Integer)
    Weight = SQLAlchemy.Column(SQLAlchemy.Integer)
    Age = SQLAlchemy.Column(SQLAlchemy.Integer)
    Gender = SQLAlchemy.Column(SQLAlchemy.String(50))
    Blood_Pressure = SQLAlchemy.Column(SQLAlchemy.Integer)
    Medication = SQLAlchemy.Column(SQLAlchemy.Text)
    Symptoms = SQLAlchemy.Column(SQLAlchemy.Text)
    Reason_for_visit = SQLAlchemy.Column(SQLAlchemy.Text)
    Last_Reason_for_visit = SQLAlchemy.Column(SQLAlchemy.Text)
    Doctor_in_care = SQLAlchemy.Column(SQLAlchemy.Integer)

class Patient(SQLAlchemy.Model):
    __tablename__ = 'Patient'
    Patient_ID = SQLAlchemy.Column(SQLAlchemy.Integer, primary_key=True)
    Paitent_Acct = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey("User_Account.User_ID"))
    Patient_Info = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey("Patient_Information.Patient_ID"))
    FName = SQLAlchemy.Column(SQLAlchemy.String(50))
    LName = SQLAlchemy.Column(SQLAlchemy.String(50))
    Insurance_Name = SQLAlchemy.Column(SQLAlchemy.String(255))
    Policy_Number = SQLAlchemy.Column(SQLAlchemy.Integer)
    Covered = SQLAlchemy.Column(SQLAlchemy.Boolean)
    Phone = SQLAlchemy.Column(SQLAlchemy.String(15))
    Address = SQLAlchemy.Column(SQLAlchemy.String(255))
    EContact_Name = SQLAlchemy.Column(SQLAlchemy.String(50))
    EContact_Phone = SQLAlchemy.Column(SQLAlchemy.String(15))
    Current_Balance = SQLAlchemy.Column(SQLAlchemy.Float)


    def __init__(self, user_account, fname, lname, insurance, policy_num, phone, address, econtact, econ_num):
        self.Paitent_Acct = user_account
        self.FName = fname
        self.LName = lname
        self.Insurance_Name = insurance
        self.Policy_Number = policy_num
        self.Phone = phone
        self.Address = address
        self.EContact_Name = econtact
        self.EContact_Phone = econ_num

class Employee(SQLAlchemy.Model):
    __tablename__ = 'Employee'
    Employee_ID = SQLAlchemy.Column(SQLAlchemy.Integer, primary_key=True)
    Position = SQLAlchemy.Column(SQLAlchemy.String(50))
    FName = SQLAlchemy.Column(SQLAlchemy.String(50))
    LName = SQLAlchemy.Column(SQLAlchemy.String(50))
    HiredDate = SQLAlchemy.Column(SQLAlchemy.Date)
    PTO = SQLAlchemy.Column(SQLAlchemy.Integer)
    Sick_Days = SQLAlchemy.Column(SQLAlchemy.Integer)

class EmployeeSchedule(SQLAlchemy.Model):
    __tablename__ = 'Employee_schedule'
    Employee_ID = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey('Employee.Employee_ID'), primary_key=True)
    Date = SQLAlchemy.Column(SQLAlchemy.Date, primary_key=True)
    Time = SQLAlchemy.Column(SQLAlchemy.Time, primary_key=True)

class Schedule(SQLAlchemy.Model):
    __tablename__ = 'Schedule'
    Patient_ID = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey('Patient.Patient_ID'), primary_key=True)
    Employee_ID = SQLAlchemy.Column(SQLAlchemy.Integer, SQLAlchemy.ForeignKey('Employee.Employee_ID'), primary_key=True)
    Date = SQLAlchemy.Column(SQLAlchemy.Date, primary_key=True)
    Time = SQLAlchemy.Column(SQLAlchemy.Time, primary_key=True)
    Type_of_visit = SQLAlchemy.Column(SQLAlchemy.String(50))
