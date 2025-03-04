from rest_framework import serializers
from .models import SpecialtyEvent


class SpecialtyEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialtyEvent
        fields = '__all__'
