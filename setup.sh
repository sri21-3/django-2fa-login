#!/bin/bash

# 2FA Email Login System Setup Script
echo "🚀 Setting up 2FA Email Login System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

print_status "Docker and Python are installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt
print_status "Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating .env file from template..."
    cp env.example .env
    print_warning "Please edit .env file with your email server details before continuing"
    print_info "You can use the following email providers:"
    echo "  - Gmail (for development)"
    echo "  - SendGrid (for production)"
    echo "  - Mailtrap (for testing)"
    echo "  - Custom SMTP server"
    echo ""
    read -p "Press Enter to continue after editing .env file..."
fi

# Start Docker services
print_info "Starting Docker services (PostgreSQL and Redis)..."
docker-compose up -d
print_status "Docker services started"

# Wait for database to be ready
print_info "Waiting for database to be ready..."
sleep 10

# Run Django migrations
print_info "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate
print_status "Database migrations completed"

# Create superuser
print_info "Creating superuser account..."
echo "Please create a superuser account for admin access:"
python manage.py createsuperuser

# Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput
print_status "Static files collected"

print_status "Setup completed successfully!"
echo ""
print_info "To start the development server:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
print_info "To stop Docker services:"
echo "  docker-compose down"
echo ""
print_info "Admin panel: http://localhost:8000/admin/"
print_info "Application: http://localhost:8000/"

