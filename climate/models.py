from django.db import models

class ClimatePrediction(models.Model):
    image = models.ImageField(upload_to='uploads/')
    prediction = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prediction
