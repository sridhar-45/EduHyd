from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Institute, InstitutePhoto

# Inline for Institute Photos
class InstitutePhotoInline(admin.TabularInline):
    """Show photos inside institute edit page"""
    model = InstitutePhoto
    extra = 3
    fields = ['photo', 'caption']
    readonly_fields = ['uploaded_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    list_display = ['name', 'slug', 'icon', 'id']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    """Institute Admin"""
    
    list_display = [
        'name', 'get_owner_name', 'area', 'city', 'category', 
        'status', 'is_featured', 'created_at'
    ]
    
    list_filter = [
        'status', 'is_featured', 'category', 
        'city', 'area', 'created_at'
    ]
    
    search_fields = [
        'name', 'email', 'phone', 'area', 
        'description', 'owner__username', 'owner__email'
    ]
    
    list_editable = ['status', 'is_featured']
    
    prepopulated_fields = {'slug': ('name',)}
    
    list_per_page = 25
    
    ordering = ['-created_at']
    
    readonly_fields = ['created_at', 'updated_at', 'get_average_rating', 'get_total_reviews']
    
    inlines = [InstitutePhotoInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'slug', 'description', 'logo', 'category')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Location', {
            'fields': ('address', 'area', 'city', 'pincode', 'latitude', 'longitude')
        }),
        ('Other Info', {
            'fields': ('established_year', 'status', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('get_average_rating', 'get_total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_institutes', 'block_institutes', 'make_featured', 'remove_featured']
    
    def get_owner_name(self, obj):
        return obj.owner.username
    get_owner_name.short_description = 'Owner'
    get_owner_name.admin_order_field = 'owner__username'
    
    def get_average_rating(self, obj):
        avg = obj.average_rating()
        if avg > 0:
            stars = '⭐' * int(avg)
            return f"{stars} {avg:.1f}"
        return "No ratings yet"
    get_average_rating.short_description = 'Average Rating'
    
    def get_total_reviews(self, obj):
        count = obj.total_reviews()
        return f"{count} review{'s' if count != 1 else ''}"
    get_total_reviews.short_description = 'Total Reviews'
    
    def approve_institutes(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} institute(s) approved successfully.', 'success')
    approve_institutes.short_description = "✅ Approve selected institutes"
    
    def block_institutes(self, request, queryset):
        updated = queryset.update(status='blocked')
        self.message_user(request, f'{updated} institute(s) blocked.', 'warning')
    block_institutes.short_description = "🚫 Block selected institutes"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} institute(s) marked as featured.', 'success')
    make_featured.short_description = "⭐ Mark as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} institute(s) removed from featured.', 'info')
    remove_featured.short_description = "Remove from featured"

@admin.register(InstitutePhoto)
class InstitutePhotoAdmin(admin.ModelAdmin):
    """Institute Photo Admin"""
    
    list_display = ['get_institute_name', 'caption', 'uploaded_at', 'get_photo_thumbnail']
    
    list_filter = ['uploaded_at']
    
    search_fields = ['institute__name', 'caption']
    
    readonly_fields = ['uploaded_at', 'get_photo_preview']
    
    list_per_page = 30
    
    ordering = ['-uploaded_at']
    
    def get_institute_name(self, obj):
        """Display institute name"""
        return obj.institute.name
    get_institute_name.short_description = 'Institute'
    get_institute_name.admin_order_field = 'institute__name'
    
    def get_photo_thumbnail(self, obj):
        """Show small image thumbnail in list view"""
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px; border: 1px solid #ddd;" />',
                obj.photo.url
            )
        return "No Image"
    get_photo_thumbnail.short_description = 'Preview'
    
    def get_photo_preview(self, obj):
        """Show full size image preview in detail view"""
        if obj.photo:
            return format_html(
                '<div style="margin: 10px 0;"><img src="{}" style="max-width: 500px; max-height: 500px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" /></div>',
                obj.photo.url
            )
        return "No Image"
    get_photo_preview.short_description = 'Photo Preview'