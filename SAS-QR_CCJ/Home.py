import tkinter as tk
from tkinter import font
from QRScanner import QRScanner 

class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Home")
        self.geometry("500x300")
        self.configure(bg="#8B0000")  # Dark red background

        self.center_window(500,300)
        
        # Header Panel
        header_frame = tk.Frame(self, bg="#F2EEE9", height=80)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="WELCOME!", font=("Serif", 24, "bold"), bg="#F2EEE9")
        header_label.pack(pady=20)
        
      # Divider Panel
        divider = tk.Frame(self, bg="#F2EEE9", height=10)
        divider.place(x=0, y=90, width=500, height=10)

        
        # Button Panel
        
        button_frame = tk.Frame(self, bg="#F2EEE9")
      #  button_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)

        button_frame.place(x=0, y=100, width=500, height=300)
        
      #  button_frame.pack(fill=tk.X, expand=True)

        
        button_frame.grid_columnconfigure(0, weight=1)  # Center buttons
        
        scan_btn = tk.Button(button_frame, text="SCAN ATTENDANCE", font=("Segoe UI", 12, "bold"),
                             bg="#B33A3A", fg="white", width=20, height=2, command=self.scan_attendance)
        scan_btn.grid(row=0, column=0, pady=10, padx=20, sticky="ew")  

        admin_btn = tk.Button(button_frame, text="ADMIN LOGIN", font=("Segoe UI", 12, "bold"),
                              bg="#B33A3A", fg="white", width=20, height=2, command=self.admin_login)
        admin_btn.grid(row=1, column=0, pady=10, padx=20, sticky="ew")  

    def scan_attendance(self):
        qr_window = QRScanner(self)  # Open QRScanner as a new window
        self.withdraw()
       
    def admin_login(self):
        print("Admin Login button clicked!")

    def center_window(self, width, height):
        """ Centers the window on the screen """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        
if __name__ == "__main__":
    app = Home()
    app.mainloop()
