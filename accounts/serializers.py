from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}
        

