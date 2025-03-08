import tkinter as tk
from tkinter import font
from QRScanner import QRScanner 
from Login import Login

class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home")
        self.geometry("500x350")
        self.configure(bg="#8B0000") 
        self.resizable(False, False)

        self.center_window(500,350)                          
        
        header_frame = tk.Frame(self, bg="#8B0000", height=100)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="UNIVERSITY TRACKER", font=("Georgia", 24, "bold"), bg="#8B0000", fg="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        divider = tk.Frame(self, bg="#F2EEE9")
        divider.place(x=0, y=100, width=500, height=5)

        divider2 = tk.Frame(self, bg="#F2EEE9")
        divider2.place(x=0, y=110, width=500, height=5)

        button_frame = tk.Frame(self, bg="#F2EEE9")
        button_frame.place(x=0, y=120, width=500, height=240)
        
        scan_btn = tk.Button(button_frame, text="Scan Attendance", font=("Segoe UI", 14, "bold"),
                             bg="#8B0000", fg="white", command=self.scan_attendance)
        scan_btn.place(x=150, y=40, width=200, height=50) 

        admin_btn = tk.Button(button_frame, text="Admin Login", font=("Segoe UI", 14, "bold"),
                              bg="#8B0000", fg="white", command=self.admin_login)
        admin_btn.place(x=150, y=110, width=200, height=50)

    def scan_attendance(self):
        qr_window = QRScanner(self)  
        self.withdraw()
        
       
    def admin_login(self):
        login = Login(self)
        self.withdraw()
        

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
if __name__ == "__main__":
    app = Home()
    app.mainloop()
