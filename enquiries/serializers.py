from rest_framework import serializers
from .models import Enquiry

class EnquirySerializer(serializers.ModelSerializer):
    """Enquiry Serializer"""
    institute_name = serializers.CharField(source='institute.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Enquiry
        fields = [
            'id', 'student_name', 'email', 'phone',
            'institute', 'institute_name', 'course', 'course_name',
            'message', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']