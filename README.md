
# 🚨 Missing Person Detection System

## 📌 Description

This project is a web-based Missing Person Detection System developed using Python and Flask. It uses face recognition to identify missing persons in real-time through a webcam and sends SMS alerts using Twilio when a match is found.

---

## 🚀 Features

* 📝 Register missing person details (Name, Location, Phone, Image)
* 🎥 Real-time face detection using webcam
* 🧠 Face recognition using `face_recognition` library
* 📩 SMS alert system using Twilio API
* 📊 Data storage using CSV file
* 🌐 Simple web interface using Flask

---

## 🛠️ Technologies Used

* Python
* Flask
* OpenCV
* face_recognition
* Twilio API
* HTML

---

## 📂 Project Structure

missing_person_project/
│
├── app.py
├── data.csv
├── known_faces/
├── templates/
│   ├── index.html
│   ├── register.html
│
├── screenshots/
│   ├── home.png
│   ├── register.png
│   ├── sms.png
│
└── README.md

---

## 📷 Output Screenshots

### 🟢 Home Page

Main interface with options to register a missing person or start detection.

![Home](screenshots/home.png)

---

### 🔵 Register Missing Person

Form to enter details like name, location, phone number, and upload image.

![Register](screenshots/register.png)

---

### 📩 SMS Alert System

Sends SMS notification when a missing person is detected successfully.

![SMS](screenshots/sms.png)

---

## ▶️ How to Run

1. Install required libraries:

```
pip install flask opencv-python face-recognition twilio
```

2. Run the application:

```
python app.py
```

3. Open browser:

```
http://127.0.0.1:5000/
```

---

## 🔐 Important Note

Before running the project, update your Twilio credentials in `app.py`:

```
account_sid = "YOUR_SID"
auth_token = "YOUR_TOKEN"
twilio_number = "YOUR_TWILIO_NUMBER"
```

---

## 🎯 Future Improvements

* Deploy on cloud (Render / AWS)
* Add database (MySQL / MongoDB)
* Improve UI design
* Add multiple camera support


