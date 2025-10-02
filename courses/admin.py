from django.contrib import admin
from .models import Course
from institutes.models import Institute  # ← This import was missing!

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course Admin"""
    
    list_display = [
        'name', 'get_institute_name', 'category', 'duration', 
        'fees', 'mode', 'is_active', 'created_at'
    ]
    
    list_filter = [
        'mode', 'is_active', 'category', 'created_at'
    ]
    
    search_fields = [
        'name', 'category', 'description', 
        'institute__name'
    ]
    
    list_editable = ['is_active', 'fees']
    
    prepopulated_fields = {'slug': ('name',)}
    
    list_per_page = 30
    
    ordering = ['-created_at']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('institute', 'name', 'slug', 'description', 'category')
        }),
        ('Course Details', {
            'fields': ('duration', 'fees', 'mode', 'batch_timings', 'syllabus')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Custom method to display institute name
    def get_institute_name(self, obj):
        """Display institute name"""
        return obj.institute.name
    get_institute_name.short_description = 'Institute'
    get_institute_name.admin_order_field = 'institute__name'
    
    # Filter foreign key dropdown to show only active institutes
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Customize institute dropdown to show only active institutes"""
        if db_field.name == "institute":
            kwargs["queryset"] = Institute.objects.filter(status='active')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)