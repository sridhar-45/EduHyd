from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from institutes.models import Institute

class Review(models.Model):
    """Review and rating model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='reviews')
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'institute']  # One review per user per institute
    
    def __str__(self):
        return f"{self.user.username} - {self.institute.name} ({self.rating}★)"