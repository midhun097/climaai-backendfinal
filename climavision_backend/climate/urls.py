# climate/urls.py
from django.urls import path
from . import views

urlpatterns = [
   path('predict_weather/', views.predict_weather),

]
