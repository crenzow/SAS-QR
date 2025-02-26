import tkinter as tk
from tkinter import PhotoImage

class Students(tk.Toplevel):
    def __init__(self, root):
        self.root = root
        self.root.geometry("1150x750")
        self.root.title("Dashboard UI")

        # Sidebar (Red Panel)
        self.sidebar = tk.Frame(self.root, bg="#8B0000", width=210, height=750)
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Main Content (Ivory White Panel)
        self.main_content = tk.Frame(self.root, bg="#F2EEE9", width=940, height=750)
        self.main_content.pack_propagate(False)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load CCJ Logo (Ensure image.png is in the same directory)
        self.logo_image = PhotoImage(file="200whiteLOGO.png")
        self.logo_label = tk.Label(self.sidebar, image=self.logo_image, bg="#8B0000")
        self.logo_label.pack(pady=20)

        # Sidebar Buttons
        self.create_buttons()

    def create_button(self, parent, text):
        return tk.Button(parent, text=text, font=("Arial", 12, "bold"), fg="white", bg="#B22222", 
                         relief=tk.FLAT, width=20, height=2)

    def create_buttons(self):
        buttons = ["DASHBOARD", "STUDENTS", "ATTENDANCE", "REPORTS", "LOGOUT"]
        for btn_text in buttons:
            btn = self.create_button(self.sidebar, btn_text)
            btn.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Students(root)
    root.mainloop()

    
