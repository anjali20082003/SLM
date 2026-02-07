#!/bin/bash

echo "SLM Application Deployment Script"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Copied .env.example to .env"
        echo "Please update the .env file with your production settings before continuing."
    else
        echo "No .env.example file found. Please create a .env file with your production settings."
        exit 1
    fi
fi

# Build and start the production services
echo "Starting production deployment..."
docker-compose -f docker-compose.prod.yml up -d --build

echo "Waiting for services to start..."
sleep 30

# Run migrations
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input

echo "Deployment completed!"
echo ""
echo "Your application should now be available at http://localhost"
echo ""
echo "To create a superuser account, run:"
echo "docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"