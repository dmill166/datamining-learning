# Activity 02

## MySQL Table Export to CSV

## Goal

To illustrate how to perform a typical data export of a MySQL table to a CSV file

## Steps

### Step 1 - Setup Destination Folder

Create a 'data' folder and open its permission to all users. 

```
mkdir data
chmod 777 data
```

### Step 2 - Grant FILE Permissions to a DB User 

```
GRANT FILE ON *.* TO 'hr_admin';
```

### Step 3 - Export Table Employees

Replace the path to your data folder. 

```
SELECT * FROM Employees
INTO OUTFILE '/Users/tmota/devel/teach/__21FCS390Z_DM__/activities/activity_02_csv_export/data/employees.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';
```

Verify that the table was exported successfully. 

