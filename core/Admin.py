import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk  # Import ttk for Treeview
import qrcode
from PIL import Image, ImageTk



class Admin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Properly initialize Toplevel
        self.geometry("1150x750")
        self.title("Dashboard UI")

        self.center_window(1150, 750)

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
        tk.Label(self.main_content, text="Students Page", bg="#F2EEE9", font=("Segoe UI", 16)).pack(pady=20)

        # Create a Treeview widget for the table
        columns = ("srCode", "firstName", "middleName", "lastName", "email", "contactNum")
        self.tree = ttk.Treeview(self.main_content, columns=columns, show="headings")

        # Define column headings
        self.tree.heading("srCode", text="SR Code")
        self.tree.heading("firstName", text="First Name")
        self.tree.heading("middleName", text="Middle Name")
        self.tree.heading("lastName", text="Last Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("contactNum", text="Contact Number")

        # Set column widths (you can adjust these values based on your preference)
        self.tree.column("srCode", width=75, anchor=tk.W, stretch=tk.YES)
        self.tree.column("firstName", width=100, anchor=tk.W, stretch=tk.YES)
        self.tree.column("middleName", width=100, anchor=tk.W, stretch=tk.YES)
        self.tree.column("lastName", width=100, anchor=tk.W, stretch=tk.YES)
        self.tree.column("email", width=175, anchor=tk.W, stretch=tk.YES)  # Increased width for emails
        self.tree.column("contactNum", width=100, anchor=tk.W, stretch=tk.YES)

        # Add some sample data (you can replace this with actual data)
        students_data = [
            ("S001", "John", "Doe", "Smith", "21-10452@g.batstate-u.edu.ph", "1234567890"),
            ("S002", "Jane", "Mary", "Doe", "jane.doe@example.com", "0987654321")
        ]
        
        for student in students_data:
            self.tree.insert("", tk.END, values=student)

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

        viewBtn = tk.Button(self.main_content, text="View QR Code", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2)
        viewBtn.place(x=610, y=420, width=120, height=40)

        emailBtn = tk.Button(self.main_content, text="Send to Email", font=("Segoe UI", 10, "bold"), bg="#8B0000", fg="white", width=15, height=2)
        emailBtn.place(x=790, y=420, width=120, height=40)

        actions_frame = tk.Frame(self.main_content, bg="white")
        actions_frame.place(x=610,y=490,width=300,height=200)

        # Bind selection event to generate QR Code
        self.tree.bind("<<TreeviewSelect>>", self.generate_qr_code)


    def open_attendance(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="Attendance Page", bg="#F2EEE9", font=("Segoe UI", 16)).pack(pady=20)

    def open_reports(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="Reports Page", bg="#F2EEE9", font=("Segoe UI", 16)).pack(pady=20)

    def logout(self):     
        self.destroy()  # Closes the Admin window
        self.master.deiconify() 

    def generate_qr_code(self, event):
        # Get selected row
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            sr_code = item['values'][0]
            first_name = item['values'][1]
            middle_name = item['values'][2]
            last_name = item['values'][3]

            # Combine information to generate QR code content
            qr_content = f"SR Code: {sr_code}\nName: {first_name} {middle_name} {last_name}"

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

            # Convert image to tkinter PhotoImage for display
            img_tk = ImageTk.PhotoImage(img)

            # Display the QR code in the qrCode_frame
            label = tk.Label(self.qrCode_frame, image=img_tk)
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.place(x=0, y=0, width=300, height=300)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = Admin(root)
    root.mainloop()

    
