# 2FA Email Login System

A secure Django-based web application with Two-Factor Authentication (2FA) using email OTP (One-Time Password) for enhanced security.

## Features

- **User Registration & Login**: Simple email/password authentication
- **2FA with Email OTP**: 6-digit OTP sent via email for second factor authentication
- **Secure OTP Management**: OTP expires in 2 minutes and can only be used once
- **Login Attempt Tracking**: Monitor and log all login attempts for security
- **Responsive UI**: Modern, mobile-friendly interface with Bootstrap
- **Admin Panel**: Django admin interface for managing users, OTP logs, and login attempts

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Email**: SMTP (Gmail, SendGrid, etc.)
- **Security**: CSRF protection, secure sessions, password validation

## Project Structure

```
django_login_page/
├── config/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── authentication/         # Authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── email_otp.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── authentication/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── verify_otp.html
│   │   └── dashboard.html
│   └── emails/
│       ├── otp_email.html
│       └── otp_email.txt
├── manage.py
├── requirements.txt
├── env.example
└── README.md
```

## Installation & Setup

### Quick Start (Recommended)

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd django_login_page
   ```

2. **Configure email settings:**
   ```bash
   cp env.example .env
   # Edit .env with your email server details
   ```

3. **Run the automated setup:**
   ```bash
   ./setup.sh
   ```

4. **Start the application:**
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

### Manual Setup

#### 1. Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git

#### 2. Clone the Repository

```bash
git clone <repository-url>
cd django_login_page
```

#### 3. Start Database with Docker

```bash
docker-compose up -d
```

#### 4. Python Environment Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 5. Environment Configuration

Copy and edit the environment file:

```bash
cp env.example .env
```

**Configure your email settings in `.env`:**

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

# Email Settings (Choose one)
# Gmail (Development)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### 6. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 7. Test Email Configuration

```bash
python test_email.py
```

#### 8. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Usage

### User Registration

1. Visit the registration page
2. Fill in username, email, and password
3. Click "Register" to create your account

### Login with 2FA

1. Go to the login page
2. Enter your email and password
3. Check your email for the 6-digit OTP code
4. Enter the OTP code on the verification page
5. You'll be redirected to the dashboard upon successful verification

### Admin Panel

Access the admin panel at `http://localhost:8000/admin/` to:
- Manage users
- View OTP logs
- Monitor login attempts
- Configure system settings

## Security Features

- **OTP Expiry**: OTP codes expire after 2 minutes
- **Single Use**: Each OTP can only be used once
- **Rate Limiting**: Built-in protection against brute force attacks
- **Secure Sessions**: CSRF protection and secure cookie settings
- **Password Validation**: Strong password requirements
- **Login Monitoring**: Track all login attempts for security auditing

## Email Configuration

The system supports various SMTP providers:

### Gmail
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### SendGrid
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

## API Endpoints

- `GET /` - Home page (redirects to login)
- `GET /auth/login/` - Login page
- `POST /auth/login/` - Process login
- `GET /auth/register/` - Registration page
- `POST /auth/register/` - Process registration
- `GET /auth/verify-otp/` - OTP verification page
- `POST /auth/verify-otp/` - Process OTP verification
- `GET /auth/dashboard/` - User dashboard
- `GET /auth/logout/` - Logout
- `POST /auth/resend-otp/` - Resend OTP (AJAX)

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

```bash
# Install development dependencies
pip install flake8 black

# Run linting
flake8 .

# Format code
black .
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in production
2. Use a secure `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use a production database
5. Set up proper email service
6. Configure static file serving
7. Use HTTPS

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
