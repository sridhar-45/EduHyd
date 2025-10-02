from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'user_type', 'phone', 'profile_picture',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone', 'user_type'
        ]
    
    def validate(self, attrs):
        """Check passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs
    
    def create(self, validated_data):
        """Create user"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)