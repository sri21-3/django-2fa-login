"""
Email OTP functionality for 2FA authentication.
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import OTPLog

logger = logging.getLogger(__name__)


def send_otp_email(user, otp_log):
    """
    Send OTP code to user's email.
    
    Args:
        user: User instance
        otp_log: OTPLog instance containing the OTP code
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = 'Your 2FA Login Code'
        
        # Create email context
        context = {
            'user': user,
            'otp_code': otp_log.otp_code,
            'expiry_minutes': settings.OTP_EXPIRY_MINUTES,
            'site_name': '2FA Login System'
        }
        
        # Render email templates
        html_message = render_to_string('emails/otp_email.html', context)
        plain_message = render_to_string('emails/otp_email.txt', context)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"OTP email sent successfully to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")
        return False


def generate_and_send_otp(user):
    """
    Generate a new OTP and send it to the user's email.
    
    Args:
        user: User instance
    
    Returns:
        tuple: (otp_log, success) where success is bool indicating if email was sent
    """
    try:
        # Generate new OTP
        otp_log = OTPLog.generate_otp(user)
        
        # Send OTP via email
        success = send_otp_email(user, otp_log)
        
        return otp_log, success
        
    except Exception as e:
        logger.error(f"Failed to generate and send OTP for user {user.email}: {str(e)}")
        return None, False


def verify_otp(user, otp_code):
    """
    Verify the OTP code for a user.
    
    Args:
        user: User instance
        otp_code: 6-digit OTP code to verify
    
    Returns:
        tuple: (is_valid, otp_log) where is_valid is bool and otp_log is the OTPLog instance
    """
    try:
        # Get the most recent unused OTP for the user
        otp_log = OTPLog.objects.filter(
            user=user,
            is_used=False,
            otp_code=otp_code
        ).order_by('-created_at').first()
        
        if not otp_log:
            logger.warning(f"No valid OTP found for user {user.email}")
            return False, None
        
        # Check if OTP is expired
        if otp_log.is_expired():
            logger.warning(f"OTP expired for user {user.email}")
            return False, otp_log
        
        # Mark OTP as used and verified
        otp_log.mark_as_used()
        otp_log.mark_as_verified()
        
        logger.info(f"OTP verified successfully for user {user.email}")
        return True, otp_log
        
    except Exception as e:
        logger.error(f"Failed to verify OTP for user {user.email}: {str(e)}")
        return False, None
