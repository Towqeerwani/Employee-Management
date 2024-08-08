
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        # Define the model that the serializer will be based on
        model = Employee
        
        # Specify the fields that should be included in the serialized representation
        fields = '__all__'  # Includes all fields from the Employee model

