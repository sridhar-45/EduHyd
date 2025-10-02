from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin"""
    
    list_display = [
        'get_user_name', 'get_institute_name', 'rating', 
        'is_approved', 'created_at'
    ]
    
    list_filter = [
        'rating', 'is_approved', 'created_at'
    ]
    
    search_fields = [
        'user__username', 'user__email', 
        'institute__name', 'review_text'
    ]
    
    list_editable = ['is_approved']
    
    readonly_fields = ['created_at', 'updated_at']
    
    list_per_page = 50
    
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Info', {
            'fields': ('user', 'institute', 'rating', 'review_text')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def get_user_name(self, obj):
        return obj.user.username
    get_user_name.short_description = 'User'
    get_user_name.admin_order_field = 'user__username'
    
    def get_institute_name(self, obj):
        return obj.institute.name
    get_institute_name.short_description = 'Institute'
    get_institute_name.admin_order_field = 'institute__name'
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.', 'success')
    approve_reviews.short_description = "✅ Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) hidden.', 'warning')
    disapprove_reviews.short_description = "❌ Hide selected reviews"