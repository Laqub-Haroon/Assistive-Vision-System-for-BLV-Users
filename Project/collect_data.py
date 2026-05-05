import cv2
import os
from utils import extract_landmarks

# 👉 Change label each time
LABEL = "I LOVE U"   # change to Bye, Yes, No...

SAVE_PATH = f"dataset/{LABEL}"
os.makedirs(SAVE_PATH, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0

print("Press 's' to save | 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.putText(frame, f"{LABEL} | Count: {count}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Collect Data", frame)

    key = cv2.waitKey(1)

    # SAVE IMAGE
    if key == ord('s'):
        landmarks = extract_landmarks(frame)

        if landmarks:
            file_path = os.path.join(SAVE_PATH, f"{count}.jpg")
            cv2.imwrite(file_path, frame)
            print("Saved:", file_path)
            count += 1
        else:
            print("No hand detected ❌")

    # EXIT
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()