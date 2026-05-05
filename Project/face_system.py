import cv2
import numpy as np
from numpy.linalg import norm
import os
import csv
from insightface.app import FaceAnalysis

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

image_folder = "faces"
meta_file = "meta_data.csv"

known_faces = {}

# 🔹 Load known faces
if os.path.exists(meta_file):
    with open(meta_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Name"].strip().lower().replace(" ", "_")
            path = os.path.join(image_folder, row["Image File Path"])

            if os.path.exists(path):
                img = cv2.imread(path)
                faces = app.get(img)
                if faces:
                    known_faces[name] = faces[0].embedding

# 🔥 USE SAME IMAGE (NO CAMERA)
img = cv2.imread("captured.jpg")

person = "unknown"

if img is not None:
    faces = app.get(img)

    if faces:
        emb = faces[0].embedding

        best_score = -1
        best_name = "unknown"

        for name, e in known_faces.items():
            score = cosine_similarity(emb, e)
            if score > best_score:
                best_score = score
                best_name = name

        if best_score > 0.5:
            person = best_name

print(person)