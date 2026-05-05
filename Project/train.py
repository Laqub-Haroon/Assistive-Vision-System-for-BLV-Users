import os
import cv2
import pandas as pd
from utils import extract_landmarks
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
import joblib

DATASET_PATH = "dataset"

data = []
labels = []

print("🔄 Processing dataset...")

valid_counts = {}

# 🔵 READ DATASET
for label in os.listdir(DATASET_PATH):
    folder = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(folder):
        continue

    count = 0

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        image = cv2.imread(path)
        if image is None:
            continue

        landmarks = extract_landmarks(image)

        if landmarks:
            data.append(landmarks)
            labels.append(label)
            count += 1
        else:
            print(f"❌ No hand detected: {path}")

    valid_counts[label] = count

print("\n✅ Valid samples per class:")
print(valid_counts)

# 🚨 CHECK EMPTY DATA
if len(data) == 0:
    print("❌ No valid data found. Check dataset.")
    exit()

# 🔵 CREATE DATAFRAME
df = pd.DataFrame(data)
df["label"] = labels

# 🔵 SHUFFLE DATA
df = shuffle(df).reset_index(drop=True)

# 🔵 SAVE CSV
df.to_csv("data.csv", index=False)
print("📁 CSV saved!")

# 🔵 FEATURES & LABELS
X = df.drop("label", axis=1)
y = df["label"]

# 🔵 TRAIN / TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔵 MODEL
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    random_state=42
)

print("\n🚀 Training model...")
model.fit(X_train, y_train)

# 🔵 EVALUATE
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n🎯 Model Accuracy: {accuracy:.2f}")

# 🔵 SAVE MODEL
joblib.dump(model, "model.pkl")
print("💾 Model saved as model.pkl")

# 🔵 CLASS DISTRIBUTION
print("\n📊 Class distribution:")
print(df["label"].value_counts())