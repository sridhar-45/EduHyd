from django.db import models
from accounts.models import User
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50) 
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Institute(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    )        

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institues')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='institute_logos/', null=True, blank=True)

    #Contact Information..
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    website = models.URLField(blank=True)

    #Address..
    address = models.TextField()
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Hyderabad')
    pincode = models.CharField(max_length=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Other Info
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    established_year = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum([r.rating for r in reviews]) / len(reviews)
        return 0
    
    def total_reviews(self):
        return self.reviews.count()
    

class InstitutePhoto(models.Model):
    Institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to="institute_photos/")
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Photo for {self.Institute.name}"
    