#!/usr/bin/env python
"""
Email configuration test script for 2FA Email Login System.
Run this script to test your email configuration before starting the application.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail.backends.console import EmailBackend


def test_email_configuration():
    """Test the email configuration."""
    print("🧪 Testing Email Configuration...")
    print("=" * 50)
    
    # Check if email settings are configured
    if not settings.EMAIL_HOST_USER:
        print("❌ EMAIL_HOST_USER is not set in your .env file")
        return False
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("❌ EMAIL_HOST_PASSWORD is not set in your .env file")
        return False
    
    print(f"✅ Email Host: {settings.EMAIL_HOST}")
    print(f"✅ Email Port: {settings.EMAIL_PORT}")
    print(f"✅ Email User: {settings.EMAIL_HOST_USER}")
    print(f"✅ From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"✅ Use TLS: {settings.EMAIL_USE_TLS}")
    
    # Test email sending
    try:
        print("\n📧 Sending test email...")
        
        # Send test email
        send_mail(
            subject='2FA Login System - Test Email',
            message='This is a test email from your 2FA Login System. If you receive this, your email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to yourself
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print(f"📬 Check your inbox: {settings.EMAIL_HOST_USER}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your email credentials in .env file")
        print("2. For Gmail, make sure you're using an App Password")
        print("3. Verify 2FA is enabled for Gmail accounts")
        print("4. Check if your firewall blocks SMTP connections")
        print("5. Try a different email provider (SendGrid, Mailtrap)")
        return False


def test_console_email():
    """Test email with console backend (for debugging)."""
    print("\n🖥️  Testing with Console Backend...")
    print("=" * 50)
    
    # Temporarily switch to console backend
    original_backend = settings.EMAIL_BACKEND
    settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    try:
        send_mail(
            subject='2FA Login System - Console Test',
            message='This email would be printed to console in debug mode.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],
            fail_silently=False,
        )
        print("✅ Console email test successful!")
        print("📝 Email content would be printed above in debug mode")
        return True
    except Exception as e:
        print(f"❌ Console email test failed: {str(e)}")
        return False
    finally:
        # Restore original backend
        settings.EMAIL_BACKEND = original_backend


def main():
    """Main test function."""
    print("🚀 2FA Email Login System - Email Configuration Test")
    print("=" * 60)
    
    # Test 1: Check configuration
    if not test_email_configuration():
        print("\n❌ Email configuration test failed!")
        print("Please fix the issues above and try again.")
        return
    
    # Test 2: Console backend test
    test_console_email()
    
    print("\n" + "=" * 60)
    print("✅ Email configuration test completed!")
    print("\n📋 Next steps:")
    print("1. Check your email inbox for the test email")
    print("2. If you received it, your email is working correctly")
    print("3. Start the Django server: python manage.py runserver")
    print("4. Test the full 2FA flow by registering and logging in")


if __name__ == '__main__':
    main()


