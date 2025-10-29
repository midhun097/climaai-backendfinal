from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os
from .models import ClimatePrediction

# ✅ Load model once
MODEL_PATH = os.path.join('climate', 'model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# ✅ Labels used during training (order matters!)
labels = ['Cloudy', 'Rainy', 'Sunny', 'Foggy']

# ✅ Icons for frontend
icons = {
    'Cloudy': '☁️',
    'Rainy': '🌧️',
    'Sunny': '☀️',
    'Foggy': '🌫️'
}

@csrf_exempt
def predict_weather(request):
    if request.method != 'POST' or 'image' not in request.FILES:
        return JsonResponse({'error': 'No image uploaded'}, status=400)

    img_file = request.FILES['image']
    img_path = f"media/uploads/{img_file.name}"
    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    try:
        # ✅ Save the uploaded file
        with open(img_path, 'wb+') as dest:
            for chunk in img_file.chunks():
                dest.write(chunk)

        # ✅ Detect model input shape automatically
        input_shape = model.input_shape[1:3]

        # ✅ Load and preprocess
        img = image.load_img(img_path, target_size=input_shape)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        # ✅ Predict
        pred = model.predict(x)
        idx = int(np.argmax(pred))
        label = labels[idx]
        confidence = round(float(np.max(pred)) * 100, 2)

        # ✅ Save prediction to DB
        ClimatePrediction.objects.create(image=img_file, prediction=label)

        # ✅ Return result
        return JsonResponse({
            'prediction': label,
            'confidence': f"{confidence}%",
            'icon': icons[label]
        })

    except Exception as e:
        print("🔥 Prediction error:", str(e))
        return JsonResponse({'error': f"Backend error: {str(e)}"}, status=500)
