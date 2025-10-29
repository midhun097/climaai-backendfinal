from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .models import ClimatePrediction

# ✅ Static labels and icons
labels = ['Cloudy', 'Rainy', 'Sunny', 'Foggy']
icons = {
    'Cloudy': '☁️',
    'Rainy': '🌧️',
    'Sunny': '☀️',
    'Foggy': '🌫️'
}

@csrf_exempt
def predict_weather(request):
    """
    Handles image upload and returns a mock weather prediction
    (works without TensorFlow for frontend testing).
    """
    if request.method != 'POST' or 'image' not in request.FILES:
        return JsonResponse({'error': 'No image uploaded'}, status=400)

    img_file = request.FILES['image']
    img_path = f"media/uploads/{img_file.name}"
    os.makedirs(os.path.dirname(img_path), exist_ok=True)

    # ✅ Save uploaded file to media/uploads/
    with open(img_path, 'wb+') as dest:
        for chunk in img_file.chunks():
            dest.write(chunk)

    # ✅ Mock prediction logic (replace with real model later if needed)
    import random
    label = random.choice(labels)
    confidence = round(random.uniform(80, 99), 2)  # Random confidence between 80–99%
    icon = icons[label]

    # ✅ Save prediction to DB
    ClimatePrediction.objects.create(image=img_file, prediction=label)

    # ✅ Return mock response
    return JsonResponse({
        'prediction': label,
        'confidence': f"{confidence}%",
        'icon': icon
    })
