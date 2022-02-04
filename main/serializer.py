from rest_framework import serializers
from .models import Todo
from authentication.models import User
# user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','id']
# todo serializer
class TodoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model= Todo
        fields ="__all__"
        

