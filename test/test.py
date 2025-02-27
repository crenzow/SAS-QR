import tkinter as tk
from tkinter import ttk, messagebox
import qrcode  # Add qrcode library for QR code generation
from PIL import Image, ImageTk  # Add PIL for image handling
import mysql.connector

class StudentDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database")

        # Create side panel
        self.side_panel = tk.Frame(root, width=200, bg="lightgray", height=500, relief="sunken", borderwidth=2)
        self.side_panel.pack(side="left", fill="y")

        # Buttons for inserting and displaying student data
        self.insert_button = tk.Button(self.side_panel, text="Insert Student", command=self.show_insert_student_ui)
        self.insert_button.pack(fill="x", padx=10, pady=10)

        self.display_button = tk.Button(self.side_panel, text="Display Students", command=self.show_display_students_ui)
        self.display_button.pack(fill="x", padx=10, pady=10)

        # Create the main content frame
        self.main_content_frame = tk.Frame(root)
        self.main_content_frame.pack(side="left", fill="both", expand=True)

        # Create the QR code display panel (300x300)
        self.qr_code_frame = tk.Frame(self.main_content_frame, width=300, height=300)
        self.qr_code_frame.grid(row=0, column=1, padx=10, pady=10)

        # Initialize the main content with the insert form
        self.show_insert_student_ui()
    

    def connect_db(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",  # Change to your MySQL host if different
                user="root",       # Your MySQL username
                password="",  # Your MySQL password
                database="student_attendance_db"  # Your database name
            )
            if connection.is_connected():
                print("Successfully connected to the database.")
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None


    def show_insert_student_ui(self):
        # Clear the main content frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Insert student form UI
        label_srCode = tk.Label(self.main_content_frame, text="Student Code")
        label_srCode.grid(row=0, column=0, padx=10, pady=10)

        self.entry_srCode = tk.Entry(self.main_content_frame)
        self.entry_srCode.grid(row=0, column=1, padx=10, pady=10)

        label_firstName = tk.Label(self.main_content_frame, text="First Name")
        label_firstName.grid(row=1, column=0, padx=10, pady=10)

        self.entry_firstName = tk.Entry(self.main_content_frame)
        self.entry_firstName.grid(row=1, column=1, padx=10, pady=10)

        label_middleName = tk.Label(self.main_content_frame, text="Middle Name")
        label_middleName.grid(row=2, column=0, padx=10, pady=10)

        self.entry_middleName = tk.Entry(self.main_content_frame)
        self.entry_middleName.grid(row=2, column=1, padx=10, pady=10)

        label_lastName = tk.Label(self.main_content_frame, text="Last Name")
        label_lastName.grid(row=3, column=0, padx=10, pady=10)

        self.entry_lastName = tk.Entry(self.main_content_frame)
        self.entry_lastName.grid(row=3, column=1, padx=10, pady=10)

        label_email = tk.Label(self.main_content_frame, text="Email")
        label_email.grid(row=4, column=0, padx=10, pady=10)

        self.entry_email = tk.Entry(self.main_content_frame)
        self.entry_email.grid(row=4, column=1, padx=10, pady=10)

        label_contactNum = tk.Label(self.main_content_frame, text="Contact Number")
        label_contactNum.grid(row=5, column=0, padx=10, pady=10)

        self.entry_contactNum = tk.Entry(self.main_content_frame)
        self.entry_contactNum.grid(row=5, column=1, padx=10, pady=10)

        button_insert = tk.Button(self.main_content_frame, text="Insert Student", command=self.insert_student)
        button_insert.grid(row=6, column=0, columnspan=2, pady=20)

    def insert_student(self):
        srCode = self.entry_srCode.get()
        firstName = self.entry_firstName.get()
        middleName = self.entry_middleName.get()
        lastName = self.entry_lastName.get()
        email = self.entry_email.get()
        contactNum = self.entry_contactNum.get()

        if not (srCode and firstName and middleName and lastName and email and contactNum):
            messagebox.showerror("Input Error", "Please fill in all fields")
            return

        db = self.connect_db()
        if db is None:
            messagebox.showerror("Connection Error", "Unable to connect to the database.")
            return

        cursor = db.cursor()

        query = """
        INSERT INTO Students (srCode, firstName, middleName, lastName, email, contactNum)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (srCode, firstName, middleName, lastName, email, contactNum)

        try:
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Student details inserted successfully")
        except Exception as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    def show_display_students_ui(self):
        # Clear the main content frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Treeview for displaying students
        columns = ("srCode", "firstName", "middleName", "lastName", "email", "contactNum")
        self.treeview = ttk.Treeview(self.main_content_frame, columns=columns, show="headings")

        # Define column headings
        self.treeview.heading("srCode", text="Student Code")
        self.treeview.heading("firstName", text="First Name")
        self.treeview.heading("middleName", text="Middle Name")
        self.treeview.heading("lastName", text="Last Name")
        self.treeview.heading("email", text="Email")
        self.treeview.heading("contactNum", text="Contact Number")

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150)

        self.treeview.grid(row=0, column=0, padx=10, pady=10)

        # Button to generate QR code
        self.generate_button = tk.Button(self.main_content_frame, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_button.grid(row=1, column=0, pady=10)

        # Label or frame for displaying the QR code
        self.qr_code_frame = tk.Frame(self.main_content_frame, width=300, height=300, bg="red")
        self.qr_code_frame.grid(row=0, column=1, padx=10, pady=10)

        # Show students
        self.show_students()

    def show_students(self):
        db = self.connect_db()
        if db is None:
            messagebox.showerror("Connection Error", "Unable to connect to the database.")
            return

        cursor = db.cursor()

        # Select only the 6 specified columns from the Students table
        query = """
        SELECT srCode, firstName, middleName, lastName, email, contactNum
        FROM Students
        """
        cursor.execute(query)
        records = cursor.fetchall()

        # Clear existing records in treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Insert the selected records into the treeview
        for record in records:
            self.treeview.insert("", "end", values=record)

        cursor.close()
        db.close()

    def on_row_select(self, event):
        # Get the selected row data
        selected_item = self.treeview.selection()
        if selected_item:
            student_data = self.treeview.item(selected_item[0])['values']
            # Generate QR code using srCode and firstName
            qr_data = f"Name: {student_data[1]} {student_data[2]} {student_data[3]}\nSR Code: {student_data[0]}"
            self.generate_qr_code(qr_data)

    def generate_qr_code(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a student from the table.")
            return

        # Retrieve the data from the selected row
        selected_data = self.treeview.item(selected_item[0], 'values')
        srCode = selected_data[0]
        firstName = selected_data[1]
        qr_data = f"Name: {firstName} {selected_data[2]} {selected_data[3]}\nSR Code: {srCode}"

        # Generate QR code from the student data
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create an image for the QR code
        img = qr.make_image(fill="black", back_color="white")

        # Convert the image to a format Tkinter can display
        img_tk = ImageTk.PhotoImage(img)

        # Display the QR code in the frame
        label = tk.Label(self.qr_code_frame, image=img_tk)
        label.image = img_tk  # Keep a reference to the image
        label.pack(fill="both", expand=True)

# Create main window
root = tk.Tk()
root.geometry("1150x750")  # Update window size to fit the layout

# Create and run the app
app = StudentDatabaseApp(root)

# Start the application
root.mainloop()
