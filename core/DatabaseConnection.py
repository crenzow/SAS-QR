import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Change to your MySQL host if different
            user="root",       # Your MySQL username
            password="",  # Your MySQL password
            database="student_attendance_db"  # Your database name
        )
        if connection.is_connected():
            print("Successfully connected to the database.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
