import os
import requests

URL = "http://127.0.0.1:5000/upload"

# Loop through all CSV files
for file in os.listdir("."):
    if file.endswith(".csv"):
        print(f"Uploading {file}...")

        with open(file, "rb") as f:
            response = requests.post(
                URL,
                files={"file": f},
                data={"expiry": 60}   # expires in 60 seconds
            )

        print("Response:", response.text)
import os
import requests

URL = "http://127.0.0.1:5000/upload"

# Loop through all CSV files
for file in os.listdir("."):
    if file.endswith(".csv"):
        print(f"Uploading {file}...")

        with open(file, "rb") as f:
            response = requests.post(
                URL,
                files={"file": f},
                data={"expiry": 60}   # expires in 60 seconds
            )

        print("Response:", response.text)