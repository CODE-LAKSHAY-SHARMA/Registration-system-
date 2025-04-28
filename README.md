# Registration-system-

Person Registration Portal - Project 
Documentation 
1. Introduction 
The Person Registration Portal is a GUI-based desktop application built 
using Python (Tkinter) and MySQL. It allows users to: 
• Register new person details (name, age, gender, email, mobile number) 
• View all registered persons in a table 
• Update existing records 
• Delete records from the database 
This documentation provides an overview of the project's features, setup, 
functionality, and usage. 
2. Features 
2.1 Core Features 
✔ CRUD Operations (Create, Read, Update, Delete) 
✔ User-Friendly GUI with a modern blue theme 
✔ Form Validation (checks for empty fields) 
✔ Real-time Database Updates 
✔ Search & Display Records in a structured table 
2.2 Additional Features 
✔ Clear Form Button (reset all fields) 
✔ Confirmation Dialogs (before deletion) 
✔ Responsive UI (scalable window size) 
✔ Error Handling (prevents crashes on invalid inputs) 
3. Technologies Used 
Category 
Technology 
Purpose 
Programming 
Python 
Backend logic 
GUI Framework 
Tkinter 
Interface design 
Database 
MySQL 
Store & manage records 
Database Connector mysql-connector-python Python-MySQL bridge 
4. Installation & Setup 
4.1 Prerequisites 
• Python 3.x installed 
• MySQL Server installed 
• MySQL Connector (pip install mysql-connector-python) 
5. Functionality & Usage 
5.1 Main Interface 
• Header: Displays the title. 
• Form Section: Input fields for name, age, gender, email, and mobile. 
• Buttons: 
o Submit: Add a new record. 
o Update: Modify an existing record. 
o Delete: Remove a record. 
o Clear: Reset form fields. 
• Records Table: Displays all registered persons. 
5.2 How to Use 
Action 
Steps 
Add New 
Person 
Fill all fields → Click Submit 
Update 
Record 
Select a record → Click Update → Modify fields → 
Click Confirm Update 
Delete Record 
Select a record → Click Delete → Confirm deletion 
View Records 
Automatically displayed in the table below the form 
Clear Form 
Click Clear to reset input fields 
6. Code Structure 
6.1 Key Functions 
Function 
Description 
Registration() 
Inserts new records into the database 
update_record() 
Fills form with selected record for editing 
confirm_update() Executes the update query 
delete_record() 
Removes the selected record 
view_records() 
Fetches and displays all records 
clear_fields() 
Clears all form inputs 
6.2 Database Queries 
Operation SQL Query 
Insert 
INSERT INTO persons VALUES (...) 
Update 
UPDATE persons SET ... WHERE id=? 
Delete 
DELETE FROM persons WHERE id=? 
Fetch All 
SELECT * FROM persons 
7. Error Handling 
• Empty Fields: Shows an error if any field is left blank. 
• Invalid Inputs: Prevents SQL errors with proper validation. 
• Delete Confirmation: Asks for confirmation before deletion. 
• Database Errors: Displays MySQL errors in user-friendly messages. 
8. Future Improvements 
• Search Functionality: Filter records by name/email. 
• Export Data: Save records to CSV/Excel. 
• Enhanced UI: Dark mode, animations. 
• More Fields: Address, occupation, etc. 
• User Authentication: Login system for admins. 
9. Conclusion 
The Person Registration Portal is a simple yet powerful application for 
managing person records in a MySQL database. It demonstrates: 
✔ Python-Tkinter GUI development 
✔ MySQL database integration 
✔ CRUD operations 
✔ User-friendly design 
This project can be extended for schools, offices, or any registration-based 
system 


# project output and Database console
![image](https://github.com/user-attachments/assets/6380c0ee-d303-4093-a420-c7bc601106bc)

# SQL database record
![image](https://github.com/user-attachments/assets/dfca296c-babb-4151-b1d2-49c6ff84e3df)
![image](https://github.com/user-attachments/assets/8c9ecebe-48e1-42cf-8351-eb582e082ec3)


