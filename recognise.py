import face_recognition
import cv2
import os
import numpy as np

video_capture = cv2.VideoCapture(1)

tayyip_image = face_recognition.load_image_file("tayyip.jpg")
tayyip_face_encoding = face_recognition.face_encodings(tayyip_image)[0]

omer_image = face_recognition.load_image_file("omer.jpg")
omer_face_encoding = face_recognition.face_encodings(omer_image)[0]

zafer_image = face_recognition.load_image_file("zafer.jpg")
zafer_face_encoding = face_recognition.face_encodings(zafer_image)[0]

turgut_image = face_recognition.load_image_file("turgut.jpg")
turgut_face_encoding = face_recognition.face_encodings(turgut_image)[0]

cem_image = face_recognition.load_image_file("cem.jpg")
cem_face_encoding = face_recognition.face_encodings(cem_image)[0]

known_face_encodings = [
    tayyip_face_encoding,
    omer_face_encoding,
    zafer_face_encoding,
    turgut_face_encoding,
    cem_face_encoding
]

known_face_names = [
    "Tayyip",
    "Omer Abim",
    "Zafer Abim",
    "Turgut",
    "Cem"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 3
        right *= 5
        bottom *= 5
        left *= 3

        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
