USE sequential_medicine;

DROP TABLE IF EXISTS Appointment_Schedule;
DROP TABLE IF EXISTS Employee_schedule;
DROP TABLE IF EXISTS Patient_Information;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Insurance;

CREATE TABLE Insurance (
    Insurance_Name VARCHAR(30) PRIMARY KEY NOT NULL,
    Policy_Number INT NOT NULL,
    Covered BOOLEAN DEFAULT FALSE,
    Deductible INT NOT NULL
);

CREATE TABLE Patient (
    Patient_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    FName VARCHAR(15) NOT NULL,
    LName VARCHAR(15) NOT NULL,
    Insurance_Name VARCHAR(30) NOT NULL,
    Covered BOOLEAN DEFAULT FALSE,
    Phone BIGINT NOT NULL,
    Address VARCHAR(50),
    EContact_Name VARCHAR(32) NOT NULL,
    EContact_Phone BIGINT NOT NULL,
    FOREIGN KEY (Insurance_Name) REFERENCES Insurance(Insurance_Name)
);

CREATE TABLE Employee (
    Employee_ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Position VARCHAR(15) NOT NULL,
    FName VARCHAR(15) NOT NULL,
    LName VARCHAR(15) NOT NULL,
    HiredDate INT NOT NULL,
    PTO INT NOT NULL,
    Sick_days INT NOT NULL
);

CREATE TABLE Patient_Information (
    Patient_ID INT UNIQUE NOT NULL,
    Height INT,
    Weight INT,
    Age INT,
    Sex VARCHAR(1),
    Blood_Preasure INT NOT NULL,
    Medication TEXT NOT NULL,
    Symptoms TEXT NOT NULL,
    Reason_for_visit TEXT NOT NULL,
    Last_Reason_for_visit TEXT,
    Doctor_in_care INT NOT NULL,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_in_care) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Employee_schedule (
    Employee_ID INT NOT NULL UNIQUE,
    Date INT NOT NULL,
    Time INT NOT NULL,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Employee_ID)
);

CREATE TABLE Appointment_Schedule (
    Patient_ID INT UNIQUE NOT NULL,
    Doctor_ID INT UNIQUE NOT NULL,
    Nurse_ID INT UNIQUE NOT NULL,
    Date INT NOT NULL,
    Time INT NOT NULL,
    Type_of_visit VARCHAR(30) NOT NULL,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Employee(Employee_ID),
    FOREIGN KEY (Nurse_ID) REFERENCES Employee(Employee_ID)
);
