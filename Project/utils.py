import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)

def extract_landmarks(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        landmarks = []

        for lm in hand.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])

        return landmarks

    return None