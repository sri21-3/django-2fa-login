# Email Configuration Guide

This guide will help you configure your email server for the 2FA Email Login System.

## Quick Setup

1. **Copy the environment file:**
   ```bash
   cp env.example .env
   ```

2. **Edit the `.env` file with your email settings**

3. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

## Email Provider Options

### 1. Gmail (Recommended for Development)

**Pros:** Easy setup, reliable delivery
**Cons:** Requires App Password, not ideal for production

**Setup Steps:**
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Update your `.env` file:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### 2. SendGrid (Recommended for Production)

**Pros:** High deliverability, detailed analytics, free tier available
**Cons:** Requires account setup

**Setup Steps:**
1. Create a SendGrid account at https://sendgrid.com
2. Verify your sender identity
3. Generate an API key
4. Update your `.env` file:

```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 3. Mailtrap (Testing Only)

**Pros:** Perfect for testing, no real emails sent
**Cons:** Not for production use

**Setup Steps:**
1. Create account at https://mailtrap.io
2. Get your SMTP credentials from inbox settings
3. Update your `.env` file:

```env
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-mailtrap-username
EMAIL_HOST_PASSWORD=your-mailtrap-password
DEFAULT_FROM_EMAIL=test@yourdomain.com
```

### 4. Custom SMTP Server

**Setup Steps:**
1. Get SMTP details from your email provider
2. Update your `.env` file:

```env
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-username
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Testing Email Configuration

After setting up your email, test it by:

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Register a new user** at http://localhost:8000/auth/register/

3. **Try logging in** - you should receive an OTP email

4. **Check the Django logs** for any email errors

## Troubleshooting

### Common Issues

**1. "SMTPAuthenticationError"**
- Check your email credentials
- For Gmail, ensure you're using an App Password, not your regular password
- Verify 2FA is enabled for Gmail

**2. "Connection refused"**
- Check if the SMTP host and port are correct
- Ensure your firewall allows the connection
- Try different ports (587, 465, 25)

**3. "Emails going to spam"**
- Use a proper "From" email address
- Set up SPF, DKIM records for your domain
- Consider using a professional email service like SendGrid

**4. "OTP not received"**
- Check spam folder
- Verify email address is correct
- Check Django logs for errors
- Test with a different email provider

### Debug Mode

To debug email issues, add this to your Django settings:

```python
# In config/settings.py
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to the console instead of sending them.

## Production Considerations

1. **Use a professional email service** (SendGrid, AWS SES, etc.)
2. **Set up proper DNS records** (SPF, DKIM, DMARC)
3. **Monitor email delivery rates**
4. **Implement email templates** with proper branding
5. **Set up email monitoring and alerts**

## Security Best Practices

1. **Never commit email credentials** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys regularly**
4. **Monitor for suspicious login attempts**
5. **Implement rate limiting** for OTP requests

## Example .env File

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (Docker)
DB_NAME=2fa_login
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=localhost
DB_PORT=5432

# Email Settings (Gmail Example)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## Need Help?

If you're still having issues:

1. Check the Django logs for detailed error messages
2. Test your email configuration with a simple Python script
3. Verify your email provider's documentation
4. Check firewall and network settings

