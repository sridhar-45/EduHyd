from rest_framework import serializers
from .models import Category, Institute, InstitutePhoto

class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description']

class InstitutePhotoSerializer(serializers.ModelSerializer):
    """Institute Photo Serializer"""
    class Meta:
        model = InstitutePhoto
        fields = ['id', 'photo', 'caption', 'uploaded_at']

class InstituteListSerializer(serializers.ModelSerializer):
    """Institute List Serializer (for listing page)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Institute
        fields = [
            'id', 'name', 'slug', 'logo', 'description',
            'area', 'city', 'category_name', 'owner_name',
            'average_rating', 'total_reviews', 'is_featured',
            'status', 'created_at'
        ]
    
    def get_average_rating(self, obj):
        return round(obj.average_rating(), 1)
    
    def get_total_reviews(self, obj):
        return obj.total_reviews()

class InstituteDetailSerializer(serializers.ModelSerializer):
    """Institute Detail Serializer (for single institute page)"""
    category = CategorySerializer(read_only=True)
    photos = InstitutePhotoSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Institute
        fields = [
            'id', 'name', 'slug', 'description', 'logo',
            'email', 'phone', 'website',
            'address', 'area', 'city', 'pincode',
            'latitude', 'longitude',
            'category', 'established_year', 'status',
            'is_featured', 'owner_name',
            'photos', 'average_rating', 'total_reviews',
            'created_at', 'updated_at'
        ]
    
    def get_average_rating(self, obj):
        return round(obj.average_rating(), 1)
    
    def get_total_reviews(self, obj):
        return obj.total_reviews()