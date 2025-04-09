# Face Recognition Attendance System

This project is a **Face Recognition-based Attendance System** developed using Python. It captures real-time video using a webcam, recognizes registered faces from a folder of images, and automatically logs attendance in a `.csv` file including the person's **name, date, and time**. It is a simple yet powerful application of computer vision and machine learning, tailored for classrooms, labs, and office environments.

---

## 🎯 Motivation

Traditional methods of taking attendance are time-consuming, error-prone, and require manual handling. This project aims to **automate attendance marking using facial recognition** to ensure accuracy, save time, and promote a contactless solution — especially useful in a post-pandemic world.

---

## 🧠 How It Works

1. **Images of known people** are stored in a folder (`Images/`).
2. The system uses the **face_recognition** library to convert each face into a **128-dimensional encoding**.
3. It activates the **webcam**, detects and encodes faces in real-time.
4. Each detected face is **compared to known encodings**.
5. If a match is found, the person’s **name, current date, and time** are recorded in a file named `Attendance.csv`.
6. The recognized face is shown on screen with a green box and label.

---

## ✅ Features

- Real-time face recognition using webcam.
- Attendance is logged automatically with **name, date, and time**.
- Prevents duplicate entries during the same session or day (optional logic).
- Shows a GUI with options to start attendance and view absentees.
- Uses OpenCV and Tkinter for visual and interface handling.

---

## 📂 Sample Attendance Output

   - Name,Date,Time
   - VISHNU,2025-04-07,15:12:45.
   - ASHRITH,2025-04-07,15:14:03.


