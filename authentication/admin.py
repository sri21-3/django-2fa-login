"""
Admin configuration for authentication app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import OTPLog, LoginAttempt


@admin.register(OTPLog)
class OTPLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_used', 'is_verified', 'is_expired_display']
    list_filter = ['is_used', 'is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'otp_code']
    readonly_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('OTP Information', {
            'fields': ('user', 'otp_code', 'created_at', 'expires_at')
        }),
        ('Status', {
            'fields': ('is_used', 'is_verified')
        }),
    )
    
    def is_expired_display(self, obj):
        """Display if OTP is expired with color coding."""
        if obj.is_expired():
            return format_html('<span style="color: red;">Expired</span>')
        else:
            return format_html('<span style="color: green;">Valid</span>')
    is_expired_display.short_description = 'Expired'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['email', 'ip_address', 'success', 'failure_reason', 'created_at', 'user_link']
    list_filter = ['success', 'created_at', 'failure_reason']
    search_fields = ['email', 'ip_address', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Login Information', {
            'fields': ('user', 'email', 'ip_address', 'user_agent')
        }),
        ('Result', {
            'fields': ('success', 'failure_reason', 'created_at')
        }),
    )
    
    def user_link(self, obj):
        """Create a link to the user's admin page."""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user')


# Customize the admin site
admin.site.site_header = "2FA Email Login System Administration"
admin.site.site_title = "2FA Admin"
admin.site.index_title = "Welcome to 2FA Email Login Administration"
