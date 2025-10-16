"""
Views for authentication app.
"""
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, LoginForm, OTPVerificationForm
from .models import LoginAttempt, OTPLog
from .email_otp import generate_and_send_otp, verify_otp

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_login_attempt(email, ip_address, user_agent, success=False, failure_reason='', user=None):
    """Log login attempt for security monitoring."""
    try:
        LoginAttempt.objects.create(
            user=user,
            email=email,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            failure_reason=failure_reason
        )
    except Exception as e:
        logger.error(f"Failed to log login attempt: {str(e)}")


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('authentication:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    """User login view - step 1: email and password."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            ip_address = get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            try:
                # Find user by email
                user = User.objects.get(email=email)
                
                # Authenticate user
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    if user.is_active:
                        # Generate and send OTP
                        otp_log, email_sent = generate_and_send_otp(user)
                        
                        if email_sent:
                            # Store user ID in session for OTP verification
                            request.session['otp_user_id'] = user.id
                            request.session['otp_log_id'] = otp_log.id
                            
                            log_login_attempt(email, ip_address, user_agent, success=True, user=user)
                            messages.success(request, f'OTP sent to {email}. Please check your email.')
                            return redirect('authentication:verify_otp')
                        else:
                            log_login_attempt(email, ip_address, user_agent, success=False, failure_reason='Email sending failed')
                            messages.error(request, 'Failed to send OTP. Please try again.')
                    else:
                        log_login_attempt(email, ip_address, user_agent, success=False, failure_reason='Account disabled')
                        messages.error(request, 'Your account is disabled.')
                else:
                    log_login_attempt(email, ip_address, user_agent, success=False, failure_reason='Invalid credentials')
                    messages.error(request, 'Invalid email or password.')
                    
            except User.DoesNotExist:
                log_login_attempt(email, ip_address, user_agent, success=False, failure_reason='User not found')
                messages.error(request, 'Invalid email or password.')
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                log_login_attempt(email, ip_address, user_agent, success=False, failure_reason='System error')
                messages.error(request, 'An error occurred. Please try again.')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})


def verify_otp_view(request):
    """OTP verification view - step 2: verify OTP code."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    
    # Check if user is in OTP verification flow
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, 'Please log in first.')
        return redirect('authentication:login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('authentication:login')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            
            # Verify OTP
            is_valid, otp_log = verify_otp(user, otp_code)
            
            if is_valid:
                # Login user
                login(request, user)
                
                # Clear session data
                request.session.pop('otp_user_id', None)
                request.session.pop('otp_log_id', None)
                
                messages.success(request, 'Login successful!')
                return redirect('authentication:dashboard')
            else:
                if otp_log and otp_log.is_expired():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                else:
                    messages.error(request, 'Invalid OTP code. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'authentication/verify_otp.html', {
        'form': form,
        'email': user.email
    })


@login_required
def dashboard_view(request):
    """User dashboard after successful login."""
    # Get recent OTP logs for the user
    recent_otps = OTPLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    return render(request, 'authentication/dashboard.html', {
        'user': request.user,
        'recent_otps': recent_otps
    })


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')


@login_required
def resend_otp_view(request):
    """Resend OTP view."""
    if request.method == 'POST':
        user_id = request.session.get('otp_user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'Invalid session'})
        
        try:
            user = User.objects.get(id=user_id)
            otp_log, email_sent = generate_and_send_otp(user)
            
            if email_sent:
                request.session['otp_log_id'] = otp_log.id
                return JsonResponse({
                    'success': True, 
                    'message': f'New OTP sent to {user.email}'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Failed to send OTP. Please try again.'
                })
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            logger.error(f"Resend OTP error: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An error occurred'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def home_view(request):
    """Home page view - redirects to login."""
    return redirect('authentication:login')
