import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from Admin import Admin
from DatabaseConnection import connect_db
import mysql.connector

class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title("Login")
        self.geometry("800x570")
        self.resizable(False, False)
        self.center_window(800,570)

        left_frame = tk.Frame(self, width=400, height=570, bg="#F2EEE9")
        left_frame.place(x=0, y=0)
        
        right_frame = tk.Frame(self, width=400, height=570, bg="#8B0000")
        right_frame.place(x=400, y=0)
        
        # CCJ
        self.logo_image = Image.open("icons/350ccjWHITE.png") 
        self.logo_image = self.logo_image.resize((350, 350), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        logo_label = tk.Label(right_frame, image=self.logo_photo, bg="#8B0000")
        logo_label.place(x=25, y=95)  
        
        # User Icon (Black 64x64)
        self.user_icon = Image.open("icons/login-avatar.png")  
        self.user_icon = self.user_icon.resize((64, 64), Image.LANCZOS)
        self.user_photo = ImageTk.PhotoImage(self.user_icon)
        user_label = tk.Label(left_frame, image=self.user_photo, bg="#F2EEE9")
        user_label.place(x=100, y=110)
        
        login_label = tk.Label(left_frame, text="LOGIN", font=("Georgia", 20, "bold"), fg="#8B0000", bg="#F2EEE9")
        login_label.place(x=170, y=120)
        
        username_label = tk.Label(left_frame, text="USERNAME", font=("Segoe UI", 10, "bold"), fg="#8B0000", bg="#F2EEE9")
        username_label.place(x=40, y=210)
        
        # Email Icon
        self.email_icon = Image.open("icons/email.png") 
        self.email_icon = self.email_icon.resize((24, 24), Image.LANCZOS)
        self.email_photo = ImageTk.PhotoImage(self.email_icon)
        email_label = tk.Label(left_frame, image=self.email_photo, bg="#F2EEE9")
        email_label.place(x=50, y=240)
        
        self.username_entry = tk.Entry(left_frame, width=30, font=("Segoe UI", 12), bd=2)
        self.username_entry.place(x=80, y=240, width=270, height=30)
        
        password_label = tk.Label(left_frame, text="PASSWORD", font=("Segoe UI", 10, "bold"), fg="#8B0000", bg="#F2EEE9")
        password_label.place(x=40, y=280)
        
        # Key Icon
        self.key_icon = Image.open("icons/key.png")  
        self.key_icon = self.key_icon.resize((24, 24), Image.LANCZOS)
        self.key_photo = ImageTk.PhotoImage(self.key_icon)
        key_label = tk.Label(left_frame, image=self.key_photo, bg="#F2EEE9")
        key_label.place(x=50, y=310)
        
        self.password_entry = tk.Entry(left_frame, width=30, font=("Segoe UI", 12), bd=2, show="*")
        self.password_entry.place(x=80, y=310, width=270, height=30)
        
        self.show_password_var = tk.BooleanVar()
        show_password = tk.Checkbutton(left_frame, text="Show Password", bg="#F2EEE9", fg="#8B0000", font=("Segoe UI", 10),
                                       variable=self.show_password_var, command=self.toggle_password)
        show_password.place(x=80, y=350)
        
        login_button = tk.Button(left_frame, text="LOGIN", font=("Segoe UI", 12, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.login)
        login_button.place(x=120, y=410, width=150, height=40)

        back_button = tk.Button(left_frame, text="Back", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.back)
        back_button.place(x=10, y=10, width=65, height=40)

        
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_password(self):
        """Toggle visibility of the password entry field."""
        if self.show_password_var.get():
            self.password_entry.config(show="")  # Show text
        else:
            self.password_entry.config(show="*")  # Hide text

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate username and password against the admin table
        if self.authenticate_user(username, password):
            # If authentication is successful, open Admin window
            Admin(self.master)
            self.destroy() 
            
        else:
            # If authentication fails, show an error message
            self.show_error_message()

    def authenticate_user(self, username, password):
        """Authenticate user credentials from the database."""
        connection = connect_db()
        if connection is None:
            return False  # If connection fails, return False
        
        cursor = connection.cursor()
        
        try:
            # Query to fetch the admin record based on the username and password
            query = "SELECT * FROM admin WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            
            result = cursor.fetchone()  # Fetch one record
            
            return result is not None  # Return True if a match is found
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")  # Print the error message
            return False
        
        finally:
            connection.close()  # Ensure the connection is always closed


    def show_error_message(self):
        error_window = tk.Toplevel(self)
        error_window.title("Login Error")
        error_window.geometry("300x150")
        error_label = tk.Label(error_window, text="Invalid username or password", fg="red", font=("Segoe UI", 12))
        error_label.pack(pady=30)
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack()

    def back(self):
        self.destroy()
        self.master.deiconify()
            
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Login(root)
    root.mainloop()
