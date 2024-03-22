CREATE DATABASE CLINICPROJECT;
USE CLINICPROJECT;


-- Adjust the Patient_Information table to include personal details and contact information
CREATE TABLE New_Patient_Information (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
    FName VARCHAR(50),
    LName VARCHAR(50),
    Height INT,
    Weight INT,
    Age INT,
    Gender VARCHAR(50),
    Blood_Pressure INT,
    Medication TEXT,
    Symptoms TEXT,
    Reason_for_visit TEXT,
    Last_Reason_for_visit TEXT,
    Doctor_in_care INT,
    Insurance_Name INT,  -- Assuming a foreign key to the Insurance table
    Phone INT,
    Address VARCHAR(255),
    EContact_Name VARCHAR(50),
    EContact_Phone INT,
    Email VARCHAR(255) UNIQUE NOT NULL,  -- To look up and communicate with patients
    FOREIGN KEY (Insurance_Name) REFERENCES Insurance(Insurance_Name),
    FOREIGN KEY (Doctor_in_care) REFERENCES Employee(Employee_ID)
);

-- Remove the separate Patient table as its contents have been merged into Patient_Information
-- ...

-- Create a User_Account table for managing login credentials
CREATE TABLE User_Account (
    User_ID INT AUTO_INCREMENT PRIMARY KEY,
    Patient_ID INT,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password_Hash CHAR(60) NOT NULL,  -- CHAR(60) is typical for bcrypt hashes
    FOREIGN KEY (Patient_ID) REFERENCES Patient_Information(Patient_ID)
);

-- Create a table for Appointments, replacing Schedule if it is used for this purpose
CREATE TABLE Appointments (
    Appointment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Patient_ID INT,
    Employee_ID INT,  -- Presumably the ID of the doctor or staff member
    Appointment_Date DATE,
    Appointment_Time TIME,
    Type_Of_Visit VARCHAR(50),
    FOREIGN KEY (Patient_ID) REFERENCES Patient_Information(Patient_ID),
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);
