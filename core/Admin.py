import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk  # Import ttk for Treeview
import qrcode
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import tkinter.simpledialog
import os
import mysql.connector
import threading  # For running the email sending in a separate thread
from tkinter import messagebox

from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
from DatabaseConnection import connect_db

class Admin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Properly initialize Toplevel
        self.geometry("1150x750")
        self.title("Dashboard UI")

        self.center_window(self, 1150, 750)
      #  self.lift()
      #  self.focus_force()

        self.sidebar = tk.Frame(self, bg="#8B0000", width=210, height=750)
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_content = tk.Frame(self, bg="#F2EEE9", width=940, height=750)
        self.main_content.pack_propagate(False)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load CCJ Logo 
        self.logo_image = PhotoImage(file="icons/200whiteLOGO.png")
        self.logo_label = tk.Label(self.sidebar, image=self.logo_image, bg="#8B0000")
        self.logo_label.pack(pady=20)

        # Sidebar Buttons
        self.create_buttons()
        self.open_students()
        

    def create_button(self, parent, text, command):
        return tk.Button(parent, text=text, font=("Segoe UI", 12, "bold"), fg="white", bg="#B33A3A", 
                         relief=tk.FLAT, width=20, height=2, command=command)

    def create_buttons(self):
        buttons = [
            ("STUDENTS", self.open_students),
            ("ATTENDANCE", self.open_attendance),
            ("REPORTS", self.open_reports),
            ("LOGOUT", self.logout)
        ]
        for text, command in buttons: 
            btn = self.create_button(self.sidebar, text, command)
            btn.pack(pady=5)

    def open_students(self):
        self.clear_main_content()
      #  tk.Label(self.main_content, text="Students Page", bg="#F2EEE9", font=("Segoe UI", 16)).pack(pady=20)

        header_label = tk.Label(self.main_content, text="Students Page", 
                                font=("Georgia", 24, "bold"), bg="#F2EEE9", fg="#8B0000")
        header_label.place(relx=0.5, y=50, anchor="center")

        # Create a Treeview widget for the table
        columns = ("srCode", "firstName", "lastName", "email", "contactNum")
        self.tree = ttk.Treeview(self.main_content, columns=columns, show="headings")

        # Define column headings
        self.tree.heading("srCode", text="SR Code")
        self.tree.heading("firstName", text="First Name")
        self.tree.heading("lastName", text="Last Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("contactNum", text="Contact Number")

        # Set column widths (you can adjust these values based on your preference)
        self.tree.column("srCode", width=75, anchor=tk.W, stretch=tk.YES)
        self.tree.column("firstName", width=100, anchor=tk.W, stretch=tk.YES)
        self.tree.column("lastName", width=100, anchor=tk.W, stretch=tk.YES)
        self.tree.column("email", width=175, anchor=tk.W, stretch=tk.YES)  # Increased width for emails
        self.tree.column("contactNum", width=100, anchor=tk.W, stretch=tk.YES)

        # Apply styling to change selected row color
        style = ttk.Style()
        style.configure("Treeview",
                        background="#f0f0f0",  # Background color of rows
                        fieldbackground="#f0f0f0",  # Background color for text field
                        foreground="black")  # Text color
        style.map("Treeview",
                  background=[('selected', '#8B0000')])  # Color for selected row (light red)

        # Create Scrollbars
        scrollbar_y = tk.Scrollbar(self.main_content, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = tk.Scrollbar(self.main_content, orient=tk.HORIZONTAL, command=self.tree.xview)

        # Attach Scrollbars to the Treeview widget
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

       # Use place to position the Treeview and Scrollbars
        self.tree.place(x=25, y=110, width=550, height=600)
        scrollbar_y.place(x=575, y=110, height=600)
        scrollbar_x.place(x=25, y=710, width=550)

        self.qrCode_frame = tk.Frame(self.main_content, bg="#8B0000")
        self.qrCode_frame.place(x=610,y=110,width=300,height=300)

        saveBtn = tk.Button(self.main_content, text="Save As", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.saveAs)
        saveBtn.place(x=620, y=420, width=120, height=40)

        self.emailBtn = tk.Button(self.main_content, text="Send Via Email", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.send_email)
        self.emailBtn.place(x=770, y=420, width=120, height=40)

        actions_frame = tk.Frame(self.main_content, bg="white")
        actions_frame.place(x=610,y=490,width=300,height=200)

        enrollBtn = tk.Button(actions_frame, text="Enroll", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.enroll)
        enrollBtn.place(relx=0.5, y=50, width=160, height=40, anchor="center")

        updateBtn = tk.Button(actions_frame, text="Update", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.saveAs)
        updateBtn.place(relx=0.5, y=100, width=160, height=40, anchor="center")

        unenrollBtn = tk.Button(actions_frame, text="Drop", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2, command=self.saveAs)
        unenrollBtn.place(relx=0.5, y=150, width=160, height=40, anchor="center")

        # Bind selection event to generate QR Code
        self.tree.bind("<<TreeviewSelect>>", self.generate_qr_code)
        self.load_students()
    
    def load_students(self):
        # Fetch data from the database
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT srCode, firstName, lastName, email, contactNum FROM students")  # Adjust the table name if needed
            students_data = cursor.fetchall()
            
            for row in self.tree.get_children():
                self.tree.delete(row)  # Clear existing rows


            # Insert data into the Treeview
            for student in students_data:
                self.tree.insert("", tk.END, values=student)
                

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    def enroll(self):
        # Open a new window to input student details
        enroll_window = tk.Toplevel(self)
        enroll_window.title("Enroll Student")
        self.center_window(enroll_window, 300, 250)  # Made window larger for spacing
        enroll_window.configure(bg="#F2EEE9")  # Set background color

        # Labels and Entry Fields
        fields = ["SR Code:", "First Name:", "Last Name:", "Email:", "Contact Number:"]
        entries = []

        for i, field in enumerate(fields):
            tk.Label(enroll_window, text=field, bg="#F2EEE9", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(enroll_window, font=("Arial", 12), width=25)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        # Function to save student info to MySQL
        def save_student():
            sr_code, first_name, last_name, email, contact = [entry.get() for entry in entries]

            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO Students (srCode, firstName, lastName, email, contactNum)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sr_code, first_name, last_name, email, contact))

                conn.commit()
                messagebox.showinfo("Success", "Student enrolled successfully!")
                self.load_students()
                enroll_window.destroy()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to enroll student: {e}")

            finally:
                conn.close()

        # Enroll Button
        enroll_button = tk.Button(enroll_window, text="Enroll", command=save_student, 
                                font=("Arial", 12, "bold"), fg="white", bg="#8B0000", 
                                padx=10, pady=5, relief="raised", width=15)
        enroll_button.grid(row=len(fields), column=0, columnspan=2, pady=15)
            

    def open_attendance(self):
        self.clear_main_content()
      #  tk.Label(self.main_content, text="Attendance Page", bg="#F2EEE9", font=("Segoe UI", 16)).pack(pady=20)

        header_label = tk.Label(self.main_content, text="Attendance Page", 
                                font=("Georgia", 24, "bold"), bg="#F2EEE9", fg="#8B0000")
        header_label.place(relx=0.5, y=50, anchor="center")

        # Create a Treeview widget for the table
        columns = ("name", "srCode", "date", "checkInTime", "checkOutTime")
        self.tree = ttk.Treeview(self.main_content, columns=columns, show="headings")

        # Define column headings
        self.tree.heading("name", text="Name")
        self.tree.heading("srCode", text="SR Code")
        self.tree.heading("date", text="Date")
        self.tree.heading("checkInTime", text="Check In Time")
        self.tree.heading("checkOutTime", text="Check Out Time")


        # Set column widths (you can adjust these values based on your preference)
        self.tree.column("name", width=150, anchor=tk.W, stretch=tk.YES)
        self.tree.column("srCode", width=150, anchor=tk.W, stretch=tk.YES)
        self.tree.column("date", width=150, anchor=tk.W, stretch=tk.YES)
        self.tree.column("checkInTime", width=150, anchor=tk.W, stretch=tk.YES)
        self.tree.column("checkOutTime", width=150, anchor=tk.W, stretch=tk.YES)  # Increased width for emails

        # Fetch data from the database
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
            SELECT CONCAT(s.firstName, ' ', s.lastName) AS fullName, 
                s.srCode, 
                DATE_FORMAT(a.date, '%M %e, %Y') AS formattedDate,
                DATE_FORMAT(a.checkInTime, '%h:%i %p') AS checkInTime, 
                DATE_FORMAT(a.checkOutTime, '%h:%i %p') AS checkOutTime
            FROM attendance a 
            JOIN students s ON a.studentID = s.studentID
        """)

            # Adjust the table name if needed
            students_data = cursor.fetchall()

            # Insert data into the Treeview
            for student in students_data:
                self.tree.insert("", tk.END, values=student)

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

        # Apply styling to change selected row color
        style = ttk.Style()
        style.configure("Treeview",
                        background="#f0f0f0",  # Background color of rows
                        fieldbackground="#f0f0f0",  # Background color for text field
                        foreground="black")  # Text color
        style.map("Treeview",
                  background=[('selected', '#8B0000')])  # Color for selected row (light red)

        # Create Scrollbars
        scrollbar_y = tk.Scrollbar(self.main_content, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = tk.Scrollbar(self.main_content, orient=tk.HORIZONTAL, command=self.tree.xview)

        # Attach Scrollbars to the Treeview widget
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

       # Use place to position the Treeview and Scrollbars
        self.tree.place(x=50, y=110, width=800, height=600)
        scrollbar_y.place(x=850, y=110, height=600)
        scrollbar_x.place(x=50, y=710, width=800)

    def open_reports(self):
        self.clear_main_content()
       # tk.Label(self.main_content, text="Reports Page", bg="#F2EEE9", font=("Segoe UI", 16)).pack(pady=20)

        header_label = tk.Label(self.main_content, text="Reports Page", 
                                font=("Georgia", 24, "bold"), bg="#F2EEE9", fg="#8B0000")
        header_label.place(relx=0.5, y=50, anchor="center")

    def logout(self):     
        self.destroy()  # Closes the Admin window
        self.master.deiconify() 

    def saveAs(self):
        if hasattr(self, "qr_code_image"):  # Check if QR code exists
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",  # Default file extension
                filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],  # Allowed file types
                title="Save QR Code"
            )
            
            if file_path:  # If the user chose a path
                self.qr_code_image.save(file_path)  # Save the image
                print(f"QR Code saved at: {file_path}")  # Show file path in console
        else:
            ("No QR code generated yet.")  # Prevent saving if no QR code exists

    def generate_qr_code(self, event):
        # Get selected row
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            sr_code = item['values'][0]
            first_name = item['values'][1]
            last_name = item['values'][2]

            # Combine information to generate QR code content
            qr_content = f"SR Code: {sr_code}\nName: {first_name} {last_name}"

            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_content)
            qr.make(fit=True)

            # Convert the QR code to an image
            img = qr.make_image(fill="black", back_color="white")
            img = img.resize((300, 300), Image.LANCZOS)  # Resize to fit into the frame

            # Save the generated image as an attribute of the class
            self.qr_code_image = img

            # Convert image to tkinter PhotoImage for display
            img_tk = ImageTk.PhotoImage(img)

            # Display the QR code in the qrCode_frame
            label = tk.Label(self.qrCode_frame, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.place(x=0, y=0, width=300, height=300)

    def former_sendEmail(self):
        # Get the email address via a simple dialog popup
        """
        email_address = tk.simpledialog.askstring("Email", "Enter the recipient's email address:")
        if not email_address:
            print("No email address provided.")
            return

        if not hasattr(self, 'qr_code_image'):
            print("No QR code generated.")
            return
        """

        # Get selected row
        selected_item = self.tree.selection()
        if not selected_item:
            print("No row selected.")
            return

        item = self.tree.item(selected_item[0])
        email_address = item['values'][3]  # Assuming email is the 4th column

        if not email_address:
            print("No email found for selected row.")
            return

        if not hasattr(self, 'qr_code_image'):
            print("No QR code generated.")
            return

        # Save the QR code image to a temporary file
        qr_img_path = "latest_qr_code.png"
        self.qr_code_image.save(qr_img_path)

        # Email setup
        sender_email = ""  # Replace with your email
        sender_password = ""  # Replace with your email password
        subject = "QR Code"
        body = "Attached is the latest generated QR code."

        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach the QR code image
        attachment = open(qr_img_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={qr_img_path}')
        msg.attach(part)
        attachment.close()

        try:
            # Establish SMTP connection
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server and port
            server.starttls()
            server.login(sender_email, sender_password)

            # Send email
            server.sendmail(sender_email, email_address, msg.as_string())
            print(f"Email sent to {email_address}")

        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

        # Optionally delete the temporary file after sending the email
        if os.path.exists(qr_img_path):
            os.remove(qr_img_path)

    def send_email(self):
        def send():
            try:
                # Disable the send button while sending
                self.emailBtn.config(state=tk.DISABLED)
              #  messagebox.showinfo("Sending", "Please wait... Sending email.")

                # Create a loading message window
                loading_window = tk.Toplevel(self.main_content)
                loading_window.title("Sending Email")
                loading_window.geometry("250x100")
                self.center_window(loading_window, 250, 100)
                loading_label = tk.Label(loading_window, text="Sending email...\nPlease wait.", font=("Segoe UI", 10))
                loading_label.pack(expand=True, padx=10, pady=10)
                loading_window.update_idletasks()  # Ensure it's shown immediately
                

                # Get selected row
                selected_item = self.tree.selection()
                if not selected_item:
                    messagebox.showwarning("No Selection", "Please select a row first.")
                    self.emailBtn.config(state=tk.NORMAL)  # Re-enable button
                    return

                item = self.tree.item(selected_item[0])
                sr_code = item['values'][0]
                email_address = item['values'][3]  # Assuming email is in the 4th column

                if not email_address:
                    loading_window.destroy()
                    messagebox.showerror("Missing Email", "No email found for the selected row.")
                    self.emailBtn.config(state=tk.NORMAL)
                    return

                if not hasattr(self, 'qr_code_image'):
                    loading_window.destroy()
                    messagebox.showerror("No QR Code", "No QR code has been generated.")
                    self.emailBtn.config(state=tk.NORMAL)
                    return

                # Save the QR code image to a temporary file
                qr_img_path = f"{sr_code}.png"
                self.qr_code_image.save(qr_img_path)

                # Email setup
                sender_email = ""  # Replace with your email
                sender_password = ""  # Replace with your email password
                subject = "QR Code"
                body = "Attached is the latest generated QR code."

                # Create email message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email_address
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Attach the QR code image
                with open(qr_img_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{qr_img_path}"')
                    msg.attach(part)

                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_address, msg.as_string())
                server.quit()

                loading_window.destroy()

                messagebox.showinfo("Success", f"Email successfully sent to {email_address}.")

            except Exception as e:
                loading_window.destroy()
                messagebox.showerror("Email Error", f"Failed to send email: {e}")

            finally:
                self.emailBtn.config(state=tk.NORMAL)  # Re-enable button after process

        # Run the sending function in a separate thread to prevent UI freezing
        threading.Thread(target=send, daemon=True).start()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def center_window(self, window, width, height):
        window.update_idletasks()  # Ensure correct dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Admin(root)
    root.mainloop()

    
