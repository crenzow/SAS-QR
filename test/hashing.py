import tkinter as tk
from tkinter import messagebox
import bcrypt
import mysql.connector

# MySQL database connection
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Your MySQL server host
            user="root",       # Your MySQL username
            password="", # Your MySQL password
            database="student_attendance_db"  # Database name
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to insert email and hashed password into the database
def insert_credentials(email, hashed_password):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        try:
            # Insert query
            query = "INSERT INTO sender_credentials (email, hashed_password) VALUES (%s, %s)"
            cursor.execute(query, (email, hashed_password))
            connection.commit()
            messagebox.showinfo("Success", "Credentials saved successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

# Function to handle form submission
def submit():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showwarning("Input Error", "Please enter both email and password.")
        return

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert the email and hashed password into the database
    insert_credentials(email, hashed_password)

# Create the UI window
window = tk.Tk()
window.title("Email and Password Hashing")
window.geometry("400x300")

# Email input
email_label = tk.Label(window, text="Email:")
email_label.pack(pady=10)
email_entry = tk.Entry(window, width=40)
email_entry.pack(pady=5)

# Password input
password_label = tk.Label(window, text="Password:")
password_label.pack(pady=10)
password_entry = tk.Entry(window, width=40, show="*")  # Hide password input
password_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.pack(pady=20)

# Start the Tkinter main loop
window.mainloop()
