import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from PIL import Image, ImageDraw
import random

# === Step 1: Generate synthetic dataset ===
print("🎨 Generating synthetic weather dataset...")

classes = ["sunny", "cloudy", "rainy", "foggy"]
num_samples_per_class = 200
img_size = 64

images = []
labels = []

for idx, label in enumerate(classes):
    for _ in range(num_samples_per_class):
        img = Image.new("RGB", (img_size, img_size), "white")
        draw = ImageDraw.Draw(img)
        
        if label == "sunny":
            draw.ellipse((20, 20, 44, 44), fill="yellow")
        elif label == "cloudy":
            draw.ellipse((10, 30, 54, 44), fill="gray")
        elif label == "rainy":
            draw.rectangle((25, 10, 40, 50), fill="blue")
        elif label == "foggy":
            draw.rectangle((0, 25, 64, 40), fill="lightgray")
        
        images.append(np.array(img))
        labels.append(idx)

images = np.array(images) / 255.0
labels = to_categorical(labels, num_classes=len(classes))

# === Step 2: Train-test split ===
X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2)

# === Step 3: Define CNN ===
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(img_size, img_size, 3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(len(classes), activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# === Step 4: Train ===
print("🚀 Training model...")
model.fit(X_train, y_train, epochs=5, validation_data=(X_val, y_val))
print("✅ Training complete!")

# === Step 5: Save model ===
os.makedirs("climate", exist_ok=True)
model_path = os.path.join("climate", "model.h5")
model.save(model_path)

print(f"🎯 Model saved successfully at: {model_path}")
