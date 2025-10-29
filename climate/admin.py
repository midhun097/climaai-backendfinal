from django.contrib import admin
from .models import ClimatePrediction

@admin.register(ClimatePrediction)
class ClimatePredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'prediction', 'created_at')
    ordering = ('-created_at',)
