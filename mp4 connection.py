import re
import mysql.connector
import os


host = "localhost"  
user = "root"  
password = "487606"  
database = "mp4" 


# Connect to the MySQL server
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Connected to the database successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

cursor = connection.cursor()

# File to process
file_path = r"C:\Users\daivi\Downloads\Radio FM 31-12-2024.m4a"  # Update with the actual file path
filename = os.path.basename(file_path)

# Function to extract date from filename
def extract_date(filename):
    match = re.search(r'\d{2}-\d{2}-\d{4}', filename)
    if match:
        
        return match.group(0)
    return None

# Extract date
extracted_date = extract_date(filename)

# Insert filename and extracted date into the database
if extracted_date:
    try:
        query = "INSERT INTO mp4_files (filename, extracted_date) VALUES (%s, %s)"
        cursor.execute(query, (filename, extracted_date))
        connection.commit()
        print("File data inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
else:
    print("No valid date found in the filename.")

# Close the database connection
cursor.close()
connection.close()

