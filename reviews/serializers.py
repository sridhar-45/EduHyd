from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    institute_name = serializers.CharField(source='institute.name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'institute', 'institute_name',
            'rating', 'review_text', 'is_approved', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Review Create Serializer"""
    class Meta:
        model = Review
        fields = ['institute', 'rating', 'review_text']
    
    def validate_rating(self, value):
        """Validate rating is between 1-5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value