from django.db import models
from institutes.models import Institute

class Course(models.Model):
    """Course model"""
    MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    )
    
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    category = models.CharField(max_length=100)
    
    # Course Details
    duration = models.CharField(max_length=100)  # "3 months", "1 year"
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    batch_timings = models.TextField(blank=True)
    syllabus = models.TextField(blank=True)
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['institute', 'slug']
    
    def __str__(self):
        return f"{self.name} - {self.institute.name}"