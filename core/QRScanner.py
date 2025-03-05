import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
from DatabaseConnection import connect_db
import time
from datetime import datetime, timedelta



class QRScanner(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("QR Scanner")
        self.geometry("1150x750")
        self.configure(bg="#F2EEE9")
        self.center_window(1150, 750)

        self.last_scan_time = {}  # Track last scan times for each student
        self.scan_cooldown = 5  # Cooldown time in seconds

        self.cap = None  # Webcam object
        self.scanning = False  # Toggle state
        self.scan_bar_pos = 0  # Position of the scan bar

        # Header
        header_frame = tk.Frame(self, bg="#8B0000", height=100)
        header_frame.pack(fill=tk.X)

        divider = tk.Frame(self, bg="#8B0000")
        divider.place(x=0, y=110, relwidth=1, height=10)

        home_btn = tk.Button(header_frame, text="Home", font=("Segoe UI", 14, "bold"),
                             bg="#B33A3A", fg="white", command=self.open_home)
        home_btn.place(relx=0.98, y=30, anchor="ne", width=100, height=40)

        header_label = tk.Label(header_frame, text="Student Attendance Scanner", 
                                font=("Georgia", 24, "bold"), bg="#8B0000", fg="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # Content Frame
        content_frame = tk.Frame(self, bg="#F2EEE9")
        content_frame.place(x=0, y=120, relwidth=1, relheight=1, height=-120)
        """
        self.webCam_frame = tk.Frame(content_frame, bg="#8B0000")
        self.webCam_frame.place(relx=0.5, rely=0.5, width=640, height=480, anchor="center")
        """
        # Video Label (Webcam Display)
        self.video_label = tk.Label(content_frame, bg="#8B0000")
        self.video_label.place(relx=0.5, rely=0.5, width=640, height=480, anchor="center")

        # CCJ
        self.logo_image = Image.open("icons/ccj500.png") 
        self.logo_image = self.logo_image.resize((500, 500), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        logo_label = tk.Label(self.video_label, image=self.logo_photo, bg="#8B0000")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # Toggle Button
        self.toggle_btn = tk.Button(content_frame, text="Enable QR Scanner", font=("Segoe UI", 14, "bold"),
                                    bg="#8B0000", fg="white", command=self.toggle_webcam)
        self.toggle_btn.place(relx=0.5, rely=0.965, width=200, height=40, anchor="s")

        self.bind("<Configure>", self.resize_webcam)

        # Bind the window close event to cleanup resources
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def open_home(self):
        self.destroy()
        self.master.deiconify()
        if self.cap:  # Check if the webcam object exists
            self.cap.release()  # Release the webcam
            self.cap = None  # Set it to None to indicate it's no longer in use

    def resize_webcam(self, event):
        """ Adjust webcam frame size when window is resized """
        if self.winfo_width() >= 1280 and self.winfo_height() >= 840:
            new_width, new_height = 1280, 720
        else:
            new_width, new_height = 640, 480

      #  self.webCam_frame.place_configure(width=new_width, height=new_height)
        self.video_label.place_configure(width=new_width, height=new_height)

    def toggle_webcam(self):
        """ Toggle webcam on/off """
        if self.scanning:
            # Stop scanning
            self.scanning = False
            self.toggle_btn.config(text="Enable QR Scanner")
            self.video_label.config(image="")  # Clear webcam display
            
            # Remove the logo if it's already displayed
            if hasattr(self, 'logo_label'):
                self.logo_label.place_forget()  # Remove the logo from the video label
                del self.logo_label  # Delete the logo label to free up resources

            # Recreate and show the logo again when stopping webcam
            self.logo_label = tk.Label(self.video_label, image=self.logo_photo, bg="#8B0000")
            self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Release the webcam if it's active
            if self.cap:
                self.cap.release()
                self.cap = None
        else:
            # Start scanning
            self.scanning = True
            self.toggle_btn.config(text="Disable QR Scanner")
            
            # Remove the logo when starting webcam
            if hasattr(self, 'logo_label'):
                self.logo_label.place_forget()  # Remove the logo before starting the webcam
                del self.logo_label  # Delete the logo label to free up resources

            # Initialize webcam
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FPS, 15)  # Limit FPS to reduce lag
            self.scan_qr_code()  # Start scanning QR codes


    def scan_qr_code(self):
        """ Capture frame, process QR codes, and update UI """
        if self.scanning and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # QR Code Detection
                for barcode in decode(frame):
                    qr_data = barcode.data.decode('utf-8')
                  # messagebox.showinfo("QR Code Scanned", f"Scanned Successfully!\nData: {qr_data}")
                    

                    # Draw bounding box
                    pts = barcode.polygon
                    if len(pts) == 4:
                        pts = [(p.x, p.y) for p in pts]
                        cv2.polylines(frame, [np.array(pts, np.int32)], True, (0, 255, 0), 2)

                    sr_code = qr_data[9:17]
                    self.process_attendance(sr_code, qr_data)
                    
                # Create the fading wind-like scanning effect
                self.create_wind_like_scanning_bar(frame)

                img = Image.fromarray(frame)
                img = img.resize((self.video_label.winfo_width(), self.video_label.winfo_height()), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                self.video_label.config(image=img_tk)
                self.video_label.image = img_tk  # Prevent garbage collection

                # Schedule next frame update
                self.after(10, self.scan_qr_code)  # Fast refresh rate
                
    def show_timed_message(self, title, message, duration=2000):  # duration in milliseconds (2000ms = 2 seconds)
        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("300x100")  # Adjust size as needed
        label = tk.Label(popup, text=message, padx=20, pady=20)
        label.pack()
        
        # Automatically close after the given duration
        popup.after(duration, popup.destroy)

    def process_attendance(self, sr_code, qr_data):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT studentID FROM students WHERE srCode = %s", (sr_code,))
        result = cursor.fetchone()

        current_time = datetime.now()
        if result:
            student_id = result[0]
            

            # Check last scan time to prevent spam
            if student_id in self.last_scan_time:
                time_since_last_scan = (current_time - self.last_scan_time[student_id]).total_seconds()
                if time_since_last_scan < self.scan_cooldown:
                    return  # Just ignore the scan without showing a message

            today = current_time.date()
            current_time_only = current_time.time()

            # Select both attendanceID and checkOutTime
            cursor.execute("SELECT attendanceID, checkOutTime FROM attendance WHERE studentID = %s AND DATE(date) = %s", (student_id, today))
            attendance = cursor.fetchone()
            
            if attendance:
                attendance_id = attendance[0]
                check_out_time = attendance[1]  # Now we correctly get the checkOutTime
                
                if check_out_time is not None:
                    self.show_timed_message("Error", f"{qr_data}\nYou have already checked out today!")
                else:
                    cursor.execute("UPDATE attendance SET checkOutTime = %s WHERE attendanceID = %s", (current_time, attendance_id))
                    self.show_timed_message("Check-Out", f"{qr_data}\nSuccessfully Checked Out!")
            else:
                cursor.execute("INSERT INTO attendance (date, checkInTime, studentID) VALUES (%s, %s, %s)", (today, current_time, student_id))
                self.show_timed_message("Check-In", f"{qr_data}\nSuccessfully Checked In!")
            
            db.commit()

            # Update last scan time for cooldown
            self.last_scan_time[student_id] = current_time

        else: 
            self.show_timed_message("Error", "Student not found!")
        self.last_scan_time[sr_code] = current_time  
        
        cursor.close()
        db.close()


    def create_wind_like_scanning_bar(self, frame):
        """ Create a moving wind-like scanning line effect with reversed fading and minimal solid part """
        bar_height = 6  # Height of the scanning bar
        wind_length = 150  # Length of the wind effect (how far it stretches)

        # Update scanning bar position with faster fluid movement
        self.scan_bar_pos += 16  # Increase step size to make the bar move faster
        if self.scan_bar_pos >= frame.shape[0]:
            self.scan_bar_pos = 0  # Reset to top once it reaches the bottom

        # Create reversed fading effect (bottom more opaque, top more transparent)
        for i in range(wind_length):
            # Small solid part at the bottom, and rest is almost invisible
            opacity = int(i * 0.3)  # Increase opacity slowly, small solid area
            opacity = min(opacity, 20)  # Limit opacity to a small value for transparency effect
            alpha = opacity / 255.0  # Normalize opacity to range [0, 1]

            # Create transparent white line
            overlay = frame.copy()
            cv2.line(overlay, (0, self.scan_bar_pos + i), (frame.shape[1], self.scan_bar_pos + i), (255, 255, 255), bar_height)

            # Blend the original frame with the transparent line (alpha transparency)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)




    def on_close(self):
        """ Handle window close (cleanup resources) """
        if self.cap:
            self.cap.release()  # Release the webcam when closing
            self.cap = None
        self.destroy()  
    

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = QRScanner(root)
    root.mainloop()
