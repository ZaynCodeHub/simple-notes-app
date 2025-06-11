from rest_framework import serializers
from .models import Note, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True} 
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'text', 'created_at', 'updated_at', 'author', 'is_public']
        read_only_fields = ['author']