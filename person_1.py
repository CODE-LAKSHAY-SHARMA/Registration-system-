import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL
try:
    con = mysql.connector.connect(
        host="localhost", user="root", password="Lakshaysh_19"
    )
    cur = con.cursor(buffered=True)
except mysql.connector.Error as e:
    messagebox.showerror(
        "Database Connection Error", f"Failed to connect to MySQL: {e}"
    )
    exit()  # Exit if database connection fails


# Create database if not exists
try:
    cur.execute("CREATE DATABASE IF NOT EXISTS registration")
    cur.execute("USE registration")
except mysql.connector.Error as e:
    messagebox.showerror("Database Error", f"Failed to create or use database: {e}")
    con.close()
    exit()

# Create tables if not exists
try:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS persons(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(20),
            age INT,
            gender VARCHAR(5),
            email VARCHAR(30),
            mobile VARCHAR(15)
        )
        """
    )

    # Address table (linked to persons)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS address(
            id INT PRIMARY KEY AUTO_INCREMENT,
            person_id INT,
            street VARCHAR(50),
            city VARCHAR(20),
            state VARCHAR(20),
            pincode VARCHAR(10),
            FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
        )
        """
    )

    # Education table (linked to persons)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS education(
            id INT PRIMARY KEY AUTO_INCREMENT,
            person_id INT,
            qualification VARCHAR(30),
            institution VARCHAR(50),
            year_completed INT,
            FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
        )
        """
    )
    con.commit()  # Commit the table creations
except mysql.connector.Error as e:
    messagebox.showerror("Table Creation Error", f"Failed to create tables: {e}")
    con.close()
    exit()


# Global variables
current_person_id = None
address_details_added = False
education_details_added = False


# Registration function
def Registration():
    global current_person_id, address_details_added, education_details_added

    if not all([e1.get(), e2.get(), e3.get(), e4.get(), e5.get()]):
        messagebox.showerror("Error", "All basic details are required!")
        return

    try:
        # Insert basic person details
        cur.execute(
            f"INSERT INTO persons(name, age, gender, email, mobile) VALUES ('{e1.get()}', '{e2.get()}', '{e3.get()}', '{e4.get()}', '{e5.get()}')"
        )
        con.commit()

        # Get the auto-generated ID of the newly inserted person
        cur.execute("SELECT LAST_INSERT_ID()")
        current_person_id = cur.fetchone()[0]

        # Reset flags for new registration
        address_details_added = False
        education_details_added = False

        # Show success and switch to address details
        messagebox.showinfo(
            "Success", "Basic details saved! Please add address details."
        )
        show_address_form()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")


# Address submission function
def submit_address():
    global address_details_added

    if not all([e6.get(), e7.get(), e8.get(), e9.get()]):
        messagebox.showerror("Error", "All address fields are required!")
        return

    try:
        cur.execute(
            f"INSERT INTO address(person_id, street, city, state, pincode) VALUES ({current_person_id}, '{e6.get()}', '{e7.get()}', '{e8.get()}', '{e9.get()}')"
        )
        con.commit()
        address_details_added = True
        messagebox.showinfo(
            "Success", "Address details saved! Please add education details."
        )
        show_education_form()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Address submission failed: {str(e)}")


# Education submission function
def submit_education():
    global education_details_added

    if not all([e10.get(), e11.get(), e12.get()]):
        messagebox.showerror("Error", "All education fields are required!")
        return

    try:
        cur.execute(
            f"INSERT INTO education(person_id, qualification, institution, year_completed) VALUES ({current_person_id}, '{e10.get()}', '{e11.get()}', '{e12.get()}')"
        )
        con.commit()
        education_details_added = True
        messagebox.showinfo("Success", "Registration complete!")
        clear_all_fields()
        view_records()
        show_person_form()  # Return to main form
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Education submission failed: {str(e)}")


# Update function
def update_record():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a record to update!")
        return

    values = tree.item(selected, "values")
    if not values:
        return

    # Store the person ID for updating related records
    global current_person_id
    current_person_id = values[0]

    # Show person details
    show_person_form()
    e1.delete(0, tk.END)
    e1.insert(0, values[1])
    e2.delete(0, tk.END)
    e2.insert(0, values[2])
    e3.delete(0, tk.END)
    e3.insert(0, values[3])
    e4.delete(0, tk.END)
    e4.insert(0, values[4])
    e5.delete(0, tk.END)
    e5.insert(0, values[5])

    # Get address details
    try:
        cur.execute(f"SELECT * FROM address WHERE person_id={current_person_id}")
        address = cur.fetchone()
        if address:
            e6.delete(0, tk.END)
            e6.insert(0, address[2])
            e7.delete(0, tk.END)
            e7.insert(0, address[3])
            e8.delete(0, tk.END)
            e8.insert(0, address[4])
            e9.delete(0, tk.END)
            e9.insert(0, address[5])
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error fetching address details: {e}")

    # Get education details
    try:
        cur.execute(f"SELECT * FROM education WHERE person_id={current_person_id}")
        education = cur.fetchone()
        if education:
            e10.delete(0, tk.END)
            e10.insert(0, education[2])
            e11.delete(0, tk.END)
            e11.insert(0, education[3])
            e12.delete(0, tk.END)
            e12.insert(0, education[4])
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error fetching education details: {e}")

    b.config(text="Confirm Update", command=lambda: confirm_update())


def confirm_update():
    try:
        # Update person details
        cur.execute(
            f"UPDATE persons SET name='{e1.get()}', age='{e2.get()}', gender='{e3.get()}', email='{e4.get()}', mobile='{e5.get()}' WHERE id={current_person_id}"
        )

        # Update or insert address details
        cur.execute(f"SELECT * FROM address WHERE person_id={current_person_id}")
        if cur.fetchone():
            cur.execute(
                f"UPDATE address SET street='{e6.get()}', city='{e7.get()}', state='{e8.get()}', pincode='{e9.get()}' WHERE person_id={current_person_id}"
            )
        else:
            cur.execute(
                f"INSERT INTO address(person_id, street, city, state, pincode) VALUES ({current_person_id}, '{e6.get()}', '{e7.get()}', '{e8.get()}', '{e9.get()}')"
            )

        # Update or insert education details
        cur.execute(f"SELECT * FROM education WHERE person_id={current_person_id}")
        if cur.fetchone():
            cur.execute(
                f"UPDATE education SET qualification='{e10.get()}', institution='{e11.get()}', year_completed='{e12.get()}' WHERE person_id={current_person_id}"
            )
        else:
            cur.execute(
                f"INSERT INTO education(person_id, qualification, institution, year_completed) VALUES ({current_person_id}, '{e10.get()}', '{e11.get()}', '{e12.get()}')"
            )

        con.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
        clear_all_fields()
        view_records()
        b.config(text="Submit Here", command=Registration)
        show_person_form()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Update failed: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


# Delete function
def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a record to delete!")
        return

    values = tree.item(selected, "values")
    if not values:
        return

    if messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete this record and all associated data?",
    ):
        try:
            # Deleting from persons table will cascade to address and education tables
            cur.execute(f"DELETE FROM persons WHERE id={values[0]}")
            con.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")
            view_records()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Delete failed: {str(e)}")


# View records function
def view_records():
    for item in tree.get_children():
        tree.delete(item)

    # Join all three tables to show comprehensive information
    try:
        cur.execute(
            """
            SELECT p.id, p.name, p.age, p.gender, p.email, p.mobile,
                   a.street, a.city, a.state, a.pincode,
                   e.qualification, e.institution, e.year_completed
            FROM persons p
            LEFT JOIN address a ON p.id = a.person_id
            LEFT JOIN education e ON p.id = e.person_id
        """
        )
        records = cur.fetchall()

        for record in records:
            tree.insert("", tk.END, values=record)
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error fetching records: {e}")


# Clear all fields function
def clear_all_fields():
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)
    e6.delete(0, tk.END)
    e7.delete(0, tk.END)
    e8.delete(0, tk.END)
    e9.delete(0, tk.END)
    e10.delete(0, tk.END)
    e11.delete(0, tk.END)
    e12.delete(0, tk.END)


# Form navigation functions
def show_person_form():
    person_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
    address_frame.grid_forget()
    education_frame.grid_forget()


def show_address_form():
    person_frame.grid_forget()
    address_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
    education_frame.grid_forget()


def show_education_form():
    person_frame.grid_forget()
    address_frame.grid_forget()
    education_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")


# GUI
win = tk.Tk()
win.geometry("1100x800")
win.title("Person Registration Portal")

# Set background color (gradient blue)
win.configure(bg="#e6f3ff")

# Custom font styles
title_font = ("Arial", 24, "bold")
label_font = ("Arial", 10, "bold")
button_font = ("Arial", 10, "bold")

# Header Frame
header_frame = tk.Frame(win, bg="#0052cc", height=80, bd=0)
header_frame.pack(fill="x", padx=0, pady=0)

# Header Label
header_label = tk.Label(
    header_frame,
    text="PERSON REGISTRATION PORTAL",
    font=title_font,
    fg="white",
    bg="#0052cc",
    pady=20,
)
header_label.pack()

# Main frame
main_frame = tk.Frame(win, bg="#e6f3ff")
main_frame.pack(pady=20)

# Person details frame
person_frame = tk.LabelFrame(
    main_frame,
    text="Person Details",
    font=label_font,
    bg="#e6f3ff",
    fg="#0052cc",
    bd=4,
    relief=tk.GROOVE,
)

# Labels for person details
l1 = tk.Label(person_frame, text="Name:", font=label_font, bg="#e6f3ff", fg="#0052cc")
l2 = tk.Label(person_frame, text="Age:", font=label_font, bg="#e6f3ff", fg="#0052cc")
l3 = tk.Label(person_frame, text="Gender:", font=label_font, bg="#e6f3ff", fg="#0052cc")
l4 = tk.Label(person_frame, text="Email:", font=label_font, bg="#e6f3ff", fg="#0052cc")
l5 = tk.Label(
    person_frame, text="Mobile Number:", font=label_font, bg="#e6f3ff", fg="#0052cc"
)

# Place Labels for person details
l1.grid(row=0, column=0, padx=10, pady=10, sticky="e")
l2.grid(row=1, column=0, padx=10, pady=10, sticky="e")
l3.grid(row=2, column=0, padx=10, pady=10, sticky="e")
l4.grid(row=3, column=0, padx=10, pady=10, sticky="e")
l5.grid(row=4, column=0, padx=10, pady=10, sticky="e")

# Entry fields for person details
e1 = tk.Entry(person_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e2 = tk.Entry(person_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e3 = tk.Entry(person_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e4 = tk.Entry(person_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e5 = tk.Entry(person_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)

# Place Entry fields for person details
e1.grid(row=0, column=1, pady=10, padx=10)
e2.grid(row=1, column=1, pady=10, padx=10)
e3.grid(row=2, column=1, pady=10, padx=10)
e4.grid(row=3, column=1, pady=10, padx=10)
e5.grid(row=4, column=1, pady=10, padx=10)

# Address details frame
address_frame = tk.LabelFrame(
    main_frame,
    text="Address Details",
    font=label_font,
    bg="#e6f3ff",
    fg="#0052cc",
    bd=4,
    relief=tk.GROOVE,
)

# Labels for address details
l6 = tk.Label(
    address_frame, text="Street:", font=label_font, bg="#e6f3ff", fg="#0052cc"
)
l7 = tk.Label(address_frame, text="City:", font=label_font, bg="#e6f3ff", fg="#0052cc")
l8 = tk.Label(address_frame, text="State:", font=label_font, bg="#e6f3ff", fg="#0052cc")
l9 = tk.Label(
    address_frame, text="Pincode:", font=label_font, bg="#e6f3ff", fg="#0052cc"
)

# Place Labels for address details
l6.grid(row=0, column=0, padx=10, pady=10, sticky="e")
l7.grid(row=1, column=0, padx=10, pady=10, sticky="e")
l8.grid(row=2, column=0, padx=10, pady=10, sticky="e")
l9.grid(row=3, column=0, padx=10, pady=10, sticky="e")

# Entry fields for address details
e6 = tk.Entry(address_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e7 = tk.Entry(address_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e8 = tk.Entry(address_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e9 = tk.Entry(address_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)

# Place Entry fields for address details
e6.grid(row=0, column=1, pady=10, padx=10)
e7.grid(row=1, column=1, pady=10, padx=10)
e8.grid(row=2, column=1, pady=10, padx=10)
e9.grid(row=3, column=1, pady=10, padx=10)

# Education details frame
education_frame = tk.LabelFrame(
    main_frame,
    text="Education Details",
    font=label_font,
    bg="#e6f3ff",
    fg="#0052cc",
    bd=4,
    relief=tk.GROOVE,
)

# Labels for education details
l10 = tk.Label(
    education_frame, text="Qualification:", font=label_font, bg="#e6f3ff", fg="#0052cc"
)
l11 = tk.Label(
    education_frame, text="Institution:", font=label_font, bg="#e6f3ff", fg="#0052cc"
)
l12 = tk.Label(
    education_frame, text="Year Completed:", font=label_font, bg="#e6f3ff", fg="#0052cc"
)

# Place Labels for education details
l10.grid(row=0, column=0, padx=10, pady=10, sticky="e")
l11.grid(row=1, column=0, padx=10, pady=10, sticky="e")
l12.grid(row=2, column=0, padx=10, pady=10, sticky="e")

# Entry fields for education details
e10 = tk.Entry(education_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e11 = tk.Entry(education_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)
e12 = tk.Entry(education_frame, width=30, font=("Arial", 10), bd=2, relief=tk.GROOVE)

# Place Entry fields for education details
e10.grid(row=0, column=1, pady=10, padx=10)
e11.grid(row=1, column=1, pady=10, padx=10)
e12.grid(row=2, column=1, pady=10, padx=10)

# Buttons frame for person details
person_button_frame = tk.Frame(person_frame, bg="#e6f3ff")
person_button_frame.grid(row=5, column=0, columnspan=2, pady=20)

# Buttons frame for address details
address_button_frame = tk.Frame(address_frame, bg="#e6f3ff")
address_button_frame.grid(row=4, column=0, columnspan=2, pady=20)

# Buttons frame for education details
education_button_frame = tk.Frame(education_frame, bg="#e6f3ff")
education_button_frame.grid(row=3, column=0, columnspan=2, pady=20)

# Button style configuration
button_style = {
    "font": button_font,
    "bg": "#0052cc",
    "fg": "white",
    "activebackground": "#003d99",
    "activeforeground": "white",
    "bd": 0,
    "padx": 15,
    "pady": 5,
    "relief": tk.RAISED,
}

# Submit Button for person details
b = tk.Button(
    person_button_frame, text="Submit Here", command=Registration, **button_style
)
b.grid(row=0, column=0, padx=5)

# Submit Button for address details
address_submit_btn = tk.Button(
    address_button_frame, text="Submit Address", command=submit_address, **button_style
)
address_submit_btn.grid(row=0, column=0, padx=5)

# Back Button for address details
address_back_btn = tk.Button(
    address_button_frame, text="Back", command=show_person_form, **button_style
)
address_back_btn.grid(row=0, column=1, padx=5)

# Submit Button for education details
education_submit_btn = tk.Button(
    education_button_frame,
    text="Submit Education",
    command=submit_education,
    **button_style,
)
education_submit_btn.grid(row=0, column=0, padx=5)

# Back Button for education details
education_back_btn = tk.Button(
    education_button_frame, text="Back", command=show_address_form, **button_style
)
education_back_btn.grid(row=0, column=1, padx=5)

# Action buttons frame (update, delete, clear)
action_button_frame = tk.Frame(person_frame, bg="#e6f3ff")
action_button_frame.grid(row=6, column=0, columnspan=2, pady=10)

# Update Button
update_btn = tk.Button(
    action_button_frame, text="Update", command=update_record, **button_style
)
update_btn.grid(row=0, column=0, padx=5)

# Delete Button
delete_btn = tk.Button(
    action_button_frame, text="Delete", command=delete_record, **button_style
)
delete_btn.grid(row=0, column=1, padx=5)

# ClearButton
clear_btn = tk.Button(
    action_button_frame, text="Clear", command=clear_all_fields, **button_style
)
clear_btn.grid(row=0, column=2, padx=5)

# Records frame
records_frame = tk.LabelFrame(
    main_frame,
    text="Registered Persons with Details",
    font=label_font,
    bg="#e6f3ff",
    fg="#0052cc",
    bd=4,
    relief=tk.GROOVE,
)
records_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# Treeview to display records
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="#0052cc")
style.configure("Treeview", font=("Arial", 9), rowheight=25)

tree = ttk.Treeview(
    records_frame,
    columns=(
        "ID",
        "Name",
        "Age",
        "Gender",
        "Email",
        "Mobile",
        "Street",
        "City",
        "State",
        "Pincode",
        "Qualification",
        "Institution",
        "Year Completed",
    ),
    show="headings",
    height=15,
)

# Configure columns
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Gender", text="Gender")
tree.heading("Email", text="Email")
tree.heading("Mobile", text="Mobile")
tree.heading("Street", text="Street")
tree.heading("City", text="City")
tree.heading("State", text="State")
tree.heading("Pincode", text="Pincode")
tree.heading("Qualification", text="Qualification")
tree.heading("Institution", text="Institution")
tree.heading("Year Completed", text="Year Completed")

tree.column("ID", width=50, anchor="center")
tree.column("Name", width=120, anchor="center")
tree.column("Age", width=50, anchor="center")
tree.column("Gender", width=70, anchor="center")
tree.column("Email", width=150, anchor="center")
tree.column("Mobile", width=100, anchor="center")
tree.column("Street", width=150, anchor="center")
tree.column("City", width=100, anchor="center")
tree.column("State", width=100, anchor="center")
tree.column("Pincode", width=80, anchor="center")
tree.column("Qualification", width=120, anchor="center")
tree.column("Institution", width=150, anchor="center")
tree.column("Year Completed", width=100, anchor="center")

# Add scrollbars
vertical_scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=tree.yview)
horizontal_scrollbar = ttk.Scrollbar(
    records_frame, orient="horizontal", command=tree.xview
)
tree.configure(
    yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set
)

vertical_scrollbar.pack(side="right", fill="y")
horizontal_scrollbar.pack(side="bottom", fill="x")
tree.pack(pady=10, fill="both", expand=True)

# Show person form initially
show_person_form()

# View records initially
view_records()

win.mainloop()
