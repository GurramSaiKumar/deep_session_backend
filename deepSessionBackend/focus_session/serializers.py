from rest_framework import serializers
from .models import NewFocusSession

class FocusSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewFocusSession
        fields = '__all__'
