#Here's the code :

import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# take images from the images folder
path = r"C:\Users\vishn\spyder programs (python)\face project\Images"
images = []
classNames = []

# code is to check whether the images folder is there or not
if not os.path.exists(path):
    os.makedirs(path)
    messagebox.showwarning("Warning", "Images folder not found. It has been created. Please add some images.")
    classNames = []
else:
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f"{path}/{cl}")      # curImg - reads each image
        if curImg is not None:
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0].upper())  # Convert to uppercase, classNames - stores names without ".jpg"



# Function to encode(converting in RGB format) faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:                                       # Check if any encoding was found
            encodeList.append(encodings[0])
    return encodeList

knownEncodings = findEncodings(images)

def markAttendance(name):
    filename = "Attendance.csv"
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    # If the file is not there, to  create a new one
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(filename, index=False)

    df = pd.read_csv(filename)

    # to ensure that csv file has correct columns
    if not {"Name", "Date", "Time"}.issubset(df.columns):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(filename, index=False)

    name = name.upper()
    df["Name"] = df["Name"].astype(str).str.upper()

    if not ((df["Name"] == name) & (df["Date"] == today_date)).any():
        new_data = pd.DataFrame([[name, today_date, current_time]], columns=["Name", "Date", "Time"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f"✅ Marked attendance for {name} at {current_time}")
    else:
        print(f"✔ {name} is already marked present today.")

# this is a function to show who are the absentees
def showAbsentees():
    filename = "Attendance.csv"
    today_date = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(filename):
        messagebox.showinfo("Absentees List", "No attendance records found.")
        return

    df = pd.read_csv(filename)

    if "Name" not in df.columns or "Date" not in df.columns:
        messagebox.showerror("Error", "Invalid attendance file format.")
        return

    df["Name"] = df["Name"].astype(str).str.upper()
    df["Date"] = df["Date"].astype(str)

    present_students = set(df[df["Date"] == today_date]["Name"].tolist())
    absentees = [student for student in classNames if student not in present_students]

    if absentees:
        messagebox.showinfo("Absentees List", "\n".join(absentees))
    else:
        messagebox.showinfo("Absentees List", "No absentees today!")

# Code/ Function  to recognize face
def recognizeFace():
    if not knownEncodings or not classNames:
        messagebox.showwarning("No Faces", "No known face encodings found. Please add images first.")
        return

    cap = cv2.VideoCapture(0)
    marked_today = set()

    while True:
        success, img = cap.read()
        if not success:
            print("❌ Could not access webcam.")
            break

        imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)                     # facesCurFrame - finds all face locations
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)    #encodesCurFrame - gives 128-dimension encodings for each face in the frame



        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(knownEncodings, encodeFace)   #matches returns a list of True/False
            faceDis = face_recognition.face_distance(knownEncodings, encodeFace)   #faceDis returns distances (smaller = better match)



            if True in matches:
                matchIndex = np.argmin(faceDis)          #matchIndex is the index of the best match
                name = classNames[matchIndex].upper()

                if name not in marked_today:
                    markAttendance(name)
                    marked_today.add(name)

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# GUI related code
def openCamera():
    messagebox.showinfo("Info", "Opening Camera for Face Recognition...")
    recognizeFace()

root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("300x250")

tk.Label(root, text="Automated Attendance System", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(root, text="Start Attendance", command=openCamera, font=("Arial", 10), bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Show Absentees", command=showAbsentees, font=("Arial", 10), bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10), bg="red", fg="white").pack(pady=5)

root.mainloop()
