import face_recognition
import os, sys
import math
from urllib.request import Request, urlopen

# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self, faces):
        self.encode_faces(faces)

    def encode_faces(self, image):
        print("Encoded faces")
        face_image = face_recognition.load_image_file(image)
        face_encoding = face_recognition.face_encodings(face_image)[0]
            
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(image)
        # print(image)

    def run_recognition(self, id):
        url = "https://drive.google.com/uc?id="+id
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        # response = urllib.request.urlopen(url)
        face_image = face_recognition.load_image_file(response)
        self.face_locations = face_recognition.face_locations(face_image)
        self.face_encodings = face_recognition.face_encodings(face_image, self.face_locations)
        self.face_names = []
        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = '???'
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                return True
                print(name)
        return False

