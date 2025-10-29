from .models import ClimatePrediction

@csrf_exempt
def recognize(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img_file = request.FILES['image']
        img_path = f"media/uploads/{img_file.name}"

        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        with open(img_path, 'wb+') as dest:
            for chunk in img_file.chunks():
                dest.write(chunk)

        try:
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img) / 255.0
            x = np.expand_dims(x, axis=0)

            prediction = model.predict(x)
            idx = np.argmax(prediction)
            label = labels[idx]
            confidence = round(float(np.max(prediction)) * 100, 2)

            # ✅ Save to DB
            ClimatePrediction.objects.create(
                image=f"uploads/{img_file.name}",
                prediction=f"{label} ({confidence}%)"
            )

            return JsonResponse({
                'icon': icons[label],
                'label': label,
                'confidence': f"{confidence}%"
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No image uploaded'}, status=400)
