from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    """Course Serializer"""
    institute_name = serializers.CharField(source='institute.name', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'slug', 'description', 'category',
            'duration', 'fees', 'mode', 'batch_timings',
            'syllabus', 'is_active', 'institute_name',
            'created_at'
        ]