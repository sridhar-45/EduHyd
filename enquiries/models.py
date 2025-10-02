from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from institutes.models import Institute
from courses.models import Course

class Enquiry(models.Model):
    """Student enquiry model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    )
    
    # Can be from registered user or guest
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='enquiries')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Contact Details (if guest)
    student_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Enquiry from {self.student_name} to {self.institute.name}"