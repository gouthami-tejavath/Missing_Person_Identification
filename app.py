from flask import Flask, render_template, request, redirect, url_for, Response
import os
import cv2
import face_recognition
import csv
from twilio.rest import Client

app = Flask(_name_)

KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

known_face_encodings = []
known_face_names = []

# 🔹 TWILIO CONFIG (REPLACE WITH YOUR DETAILS)
account_sid = "YOUR_TWILIO_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"
twilio_number = "+1234567890"

client = Client(account_sid, auth_token)

# 🔹 Load known faces
def load_known_faces():
    known_face_encodings.clear()
    known_face_names.clear()

    for file in os.listdir(KNOWN_FACES_DIR):
        if file.endswith(".jpg"):
            name = os.path.splitext(file)[0]
            image_path = os.path.join(KNOWN_FACES_DIR, file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(name)

load_known_faces()

# 🔹 Get person details
def get_person_details(name):
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["name"] == name:
                return row["phone"], row["location"]
    return None, None

# 🔹 Home
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        phone = request.form["phone"]
        image = request.files["image"]

        image.save(os.path.join(KNOWN_FACES_DIR, f"{name}.jpg"))

        with open("data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, phone, location])

        load_known_faces()
        return redirect(url_for("index"))

    return render_template("register.html")

# 🔹 Camera Detection
def gen_frames():
    camera = cv2.VideoCapture(0)
    sent_alerts = set()

    while True:
        success, frame = camera.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for (top, right, bottom, left), face_encoding in zip(locations, encodings):
            name = "Unknown"
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                index = matches.index(True)
                name = known_face_names[index]

                if name not in sent_alerts:
                    phone, location = get_person_details(name)
                    if phone:
                        client.messages.create(
                            body=f"The missing person {name} has been found at {location}",
                            from_=twilio_number,
                            to=phone
                        )
                        sent_alerts.add(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame, name, (left, top-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

# 🔹 Detect Route
@app.route("/detect")
def detect():
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if _name_ == "_main_":
    app.run(debug=True)