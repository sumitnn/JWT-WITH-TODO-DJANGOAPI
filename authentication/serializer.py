from rest_framework import serializers
from .models import User


# signup serializer
class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=12,min_length=4,write_only=True)
    class Meta:
        model= User
        fields =['email', 'password', 'username']

    def create(self, validated_data):
        return User.objects._create_user(**validated_data)
        

# Login serializer
class LoginupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model= User
        fields =['email', 'password', 'Token']
        read_only_fields= ['Token']

