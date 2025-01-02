import re
import mysql.connector
import os
import whisper
import openai

os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\ffmpeg.exe"

openai.api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxLyg4qgJbRAJR30MxRzDYPj_5P0a2_uxxxxxxxxxxxxxxxxxxxxxxSP8Y9CB7tLTtD4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxIA"

model = whisper.load_model("base")


host = "localhost"  
user = "root"  
password = "xxxxxxxxxxxxxxxxxxxxx60xxxxxxxxxxxxxxxxxxx6"  
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
    print(f"Error connecting to the database: {err}")
    exit()

cursor = connection.cursor()

# File to process
file_path = r"C:\Users\daivi\Downloads\Radio FM 31-12-2024.m4a"  
filename = os.path.basename(file_path)

# Function to extract date from filename
def extract_date(filename):
    match = re.search(r'\d{2}-\d{2}-\d{4}', filename)
    if match:
        day, month, year = match.group(0).split("-")
        return f"{year}-{month}-{day}"
    return None

# Function to transcribe audio and count the number of times an ad is mentioned
def count_ads_in_audio(file_path):
    try:
        model = whisper.load_model("base")  
        result = model.transcribe(file_path)
        transcription = result["text"].lower() 
        ad_keywords = ["radio one", "sponsored by "]
        ad_count = sum(transcription.count(keyword) for keyword in ad_keywords)
        return ad_count
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return 0 


extracted_date = extract_date(filename)


ad_count = count_ads_in_audio(file_path)

# Insert filename, extracted date, and ad count into the database
if extracted_date:
    try:
        query = "INSERT INTO mp4_files (filename, extracted_date, ad_count) VALUES (%s, %s, %s)"
        cursor.execute(query, (filename, extracted_date, ad_count))
        connection.commit()
        print("File data inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error inserting data into the database: {err}")
else:
    print("No valid date found in the filename.")

cursor.close()
connection.close()
