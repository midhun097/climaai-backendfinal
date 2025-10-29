from django.urls import path
from .views import RecognizeView

urlpatterns = [
    path('', RecognizeView.as_view(), name='recognize'),
]
