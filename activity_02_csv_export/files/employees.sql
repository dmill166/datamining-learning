USE hr;

GRANT FILE ON *.* TO 'hr_admin';

SELECT * FROM Employees
INTO OUTFILE '/Users/tmota/devel/teach/__21FCS390Z_DM__/activities/activity_02_csv_export/data/employees.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';