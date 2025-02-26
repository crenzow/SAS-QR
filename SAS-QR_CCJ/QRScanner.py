import tkinter as tk

class QRScanner(tk.Toplevel):  # Inherits from Toplevel to create a new window
    def __init__(self, parent):
        super().__init__(parent)
        self.title("QR Scanner")
        self.geometry("400x300")

        tk.Label(self, text="QR Scanner Window").pack(pady=20)
        close_btn = tk.Button(self, text="Close", command=self.destroy)
        close_btn.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = QRScanner(root)
    root.mainloop()
