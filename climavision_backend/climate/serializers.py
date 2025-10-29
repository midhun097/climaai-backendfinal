from rest_framework import serializers
from .models import ClimatePrediction

class ClimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimatePrediction
        fields = '__all__'
