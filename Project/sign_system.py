import cv2
import joblib
import mediapipe as mp
from collections import Counter

model = joblib.load("model.pkl")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

img = cv2.imread("captured.jpg")

predictions = []

rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = hands.process(rgb)

if result.multi_hand_landmarks:
    hand = result.multi_hand_landmarks[0]

    landmarks = []
    for lm in hand.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])

    pred = model.predict([landmarks])[0]
    predictions.append(pred)

if len(predictions) > 0:
    sign = Counter(predictions).most_common(1)[0][0]
else:
    sign = "none"

print(sign)