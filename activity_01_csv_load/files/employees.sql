CREATE DATABASE hr;

USE hr;

CREATE TABLE Employees (
    id     INT PRIMARY KEY, 
    name   VARCHAR(20),
    gender CHAR(1),
    email  VARCHAR(40), 
    birth  DATE, 
    start  DATE, 
    salary INT, 
    ssn    VARCHAR(11), 
    phone  VARCHAR(12)
);

CREATE USER 'hr' IDENTIFIED BY '024680';
CREATE USER 'hr_admin' IDENTIFIED BY '135791';

GRANT SELECT ON TABLE Employees TO 'hr';
GRANT ALL ON TABLE Employees TO 'hr_admin';