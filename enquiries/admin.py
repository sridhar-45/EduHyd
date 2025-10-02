from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    """Enquiry Admin"""
    
    list_display = [
        'student_name', 'email', 'phone', 
        'get_institute_name', 'get_course_name', 'status', 'created_at'
    ]
    
    list_filter = [
        'status', 'created_at'
    ]
    
    search_fields = [
        'student_name', 'email', 'phone', 
        'institute__name', 'course__name', 'message'
    ]
    
    list_editable = ['status']
    
    readonly_fields = ['created_at']
    
    list_per_page = 50
    
    ordering = ['-created_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'student_name', 'email', 'phone')
        }),
        ('Enquiry Details', {
            'fields': ('institute', 'course', 'message')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_contacted', 'mark_closed']
    
    def get_institute_name(self, obj):
        return obj.institute.name
    get_institute_name.short_description = 'Institute'
    get_institute_name.admin_order_field = 'institute__name'
    
    def get_course_name(self, obj):
        return obj.course.name if obj.course else '-'
    get_course_name.short_description = 'Course'
    
    def mark_contacted(self, request, queryset):
        updated = queryset.update(status='contacted')
        self.message_user(request, f'{updated} enquirie(s) marked as contacted.', 'success')
    mark_contacted.short_description = "📞 Mark as contacted"
    
    def mark_closed(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} enquirie(s) closed.', 'info')
    mark_closed.short_description = "✅ Mark as closed"