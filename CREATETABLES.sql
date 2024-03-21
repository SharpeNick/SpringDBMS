CREATE DATABASE CLINICPROJECT;
USE CLINICPROJECT;


CREATE TABLE Patient_Information (
    Patient_ID INT PRIMARY KEY,
    Height INT,
    Weight INT,
    Age INT,
    Gender VARCHAR(50),
    Blood_Pressure INT,
    Medication TEXT,
    Symptoms TEXT,
    Reason_for_visit TEXT,
    Last_Reason_for_visit TEXT,
    Doctor_in_care INT
);
CREATE TABLE Nurse_Form (
    Patient_ID INT PRIMARY KEY,
    Height INT,
    Weight INT,
    Age INT,
    Gender VARCHAR(50),
    Blood_Pressure INT,
    Medication TEXT,
    Symptoms TEXT,
    Doctor_in_care INT,
    FOREIGN KEY (Patient_ID) REFERENCES Patient_Information(Patient_ID)
);

-- Create Insurance table
CREATE TABLE Insurance (
    Insurance_Name INT PRIMARY KEY,
    Policy_Number INT,
    Covered BOOLEAN,
    Deductible INT
);

-- Create Patient table
CREATE TABLE Patient (
    Patient_ID INT PRIMARY KEY,
    FName VARCHAR(50),
    LName VARCHAR(50),
    Insurance_Name INT,
    Covered BOOLEAN,
    Phone INT,
    Address VARCHAR(255),
    EContact_Name VARCHAR(50),
    EContact_Phone INT,
    FOREIGN KEY (Insurance_Name) REFERENCES Insurance(Insurance_Name)
);

-- Create Employee table
CREATE TABLE Employee (
    Employee_ID INT PRIMARY KEY,
    Position VARCHAR(50),
    FName VARCHAR(50),
    LName VARCHAR(50),
    HiredDate DATE,
    PTO INT,
    Sick_Days INT
);

-- Create Employee_schedule table
CREATE TABLE Employee_schedule (
    Employee_ID INT,
    Date DATE,
    Time TIME,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

-- Create Schedule table
CREATE TABLE Schedule (
    Patient_ID INT,
    Employee_ID INT,
    Date DATE,
    Time TIME,
    Type_of_visit VARCHAR(50),
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

-- Create PatientForm table (assuming it's separate from Patient_Information)
CREATE TABLE PatientForm (
    FName VARCHAR(50),
    LName VARCHAR(50),
    Insurance_Name VARCHAR(50),
    Phone INT,
    Address VARCHAR(255),
    EContact_Name VARCHAR (50),
EContact_Phone INT,
Reason_For_Visit TEXT,
Date DATE,
Time TIME,
Type_Of_Visit VARCHAR(50)
);
    