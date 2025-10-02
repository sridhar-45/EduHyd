from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    # What fields to display in the list view
    list_display = ['username', 'email', 'user_type', 'phone', 'is_active', 'created_at']
    
    # Add filters in the sidebar
    list_filter = ['user_type', 'is_active', 'is_staff', 'created_at']
    
    # Add search functionality
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    
    # Make these fields clickable links (go to detail page)
    list_display_links = ['username', 'email']
    
    # Fields that can be edited directly in the list view
    list_editable = ['is_active']
    
    # How many items per page
    list_per_page = 25
    
    # Order by newest first
    ordering = ['-created_at']
    
    # Organize fields in the edit form
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_picture')
        }),
        ('User Type', {
            'fields': ('user_type',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fields for the "Add User" form
    add_fieldsets = (
        ('Login Info', {
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone'),
        }),
        ('User Type', {
            'fields': ('user_type',),
        }),
    )
    
    # Read-only fields (cannot be edited)
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']