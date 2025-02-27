import tkinter as tk
from tkinter import PhotoImage


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
        tk.Label(self.main_content, text="Students Page", font=("Segoe UI", 16)).pack(pady=20)

    def open_attendance(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="Attendance Page", font=("Segoe UI", 16)).pack(pady=20)

    def open_reports(self):
        self.clear_main_content()
        tk.Label(self.main_content, text="Reports Page", font=("Segoe UI", 16)).pack(pady=20)

    def logout(self):     
        self.destroy()  # Closes the Admin window
        self.master.deiconify() 

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

    
