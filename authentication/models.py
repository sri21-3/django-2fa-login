"""
Authentication models for 2FA Email Login System.
"""
import secrets
import string
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class OTPLog(models.Model):
    """
    Model to store OTP codes for 2FA authentication.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_logs')
    otp_code = models.CharField(max_length=6, help_text="6-digit OTP code")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "OTP Log"
        verbose_name_plural = "OTP Logs"
    
    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
    
    @classmethod
    def generate_otp(cls, user):
        """
        Generate a new OTP for the user.
        """
        # Generate 6-digit OTP
        otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # Calculate expiry time (2 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Create OTP record
        otp_log = cls.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        return otp_log
    
    def is_expired(self):
        """
        Check if the OTP has expired.
        """
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """
        Check if the OTP is valid (not used, not expired).
        """
        return not self.is_used and not self.is_expired()
    
    def mark_as_used(self):
        """
        Mark the OTP as used.
        """
        self.is_used = True
        self.save()
    
    def mark_as_verified(self):
        """
        Mark the OTP as verified.
        """
        self.is_verified = True
        self.save()


class LoginAttempt(models.Model):
    """
    Model to track login attempts for security monitoring.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts', null=True, blank=True)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Login Attempt"
        verbose_name_plural = "Login Attempts"
    
    def __str__(self):
        status = "Success" if self.success else f"Failed: {self.failure_reason}"
        return f"{self.email} - {status} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
