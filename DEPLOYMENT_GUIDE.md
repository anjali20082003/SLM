# Deployment Guide for SLM (Software & License Management)

This guide will help you deploy your SLM application to various cloud platforms.

## Prerequisites

1. **Environment Variables**: Create a `.env` file with the following variables:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here-at-least-50-characters-long-for-security
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=http://yourdomain.com,https://yourdomain.com

# Database Settings
DB_NAME=slm_prod_db
DB_USER=slm_user
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0

# Email Settings (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Field Encryption Key (for sensitive data)
FIELD_ENCRYPTION_KEY=your-32-character-encryption-key-here
```

Generate your secret key using Python:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deploying to Cloud Platforms

### Option 1: Deploy to Heroku

1. Install the Heroku CLI
2. Login to Heroku: `heroku login`
3. Create a new app: `heroku create your-app-name`
4. Set environment variables:
```bash
heroku config:set DJANGO_SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
# Add other environment variables as needed
```
5. Deploy: `git push heroku main`
6. Run migrations: `heroku run python manage.py migrate`
7. Create superuser: `heroku run python manage.py createsuperuser`

### Option 2: Deploy to DigitalOcean App Platform

1. Create a GitHub/GitLab repository with your code
2. Sign up for DigitalOcean
3. Create a new App and connect your repository
4. Configure environment variables in the App settings
5. Add build command: `pip install -r requirements.txt`
6. Add run command: `gunicorn config.wsgi:application`
7. Add post-deploy command: `python manage.py migrate`

### Option 3: Deploy using Docker (Self-hosted)

1. Ensure you have Docker and Docker Compose installed
2. Create your `.env` file with production settings
3. Run the following commands:

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Run initial setup (first time only)
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input
```

### Option 4: Deploy to AWS Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create application: `eb create prod-environment`
4. Set environment variables in the EB console
5. Deploy: `eb deploy`
6. Run management commands: `eb ssh` then run Django commands inside the instance

## SSL Certificate Setup

For production, you should set up SSL certificates:

### Let's Encrypt with Nginx
Update your nginx.conf to include SSL configuration:

```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # Rest of your configuration
}
```

## Post-Deployment Steps

After deploying, run these commands to initialize your application:

1. Apply database migrations:
```bash
python manage.py migrate
```

2. Create a superuser account:
```bash
python manage.py createsuperuser
```

3. Collect static files (if not done during build):
```bash
python manage.py collectstatic --noinput
```

4. Load initial data (if applicable):
```bash
python manage.py loaddata initial_data.json
```

## Monitoring and Maintenance

1. Set up logging for production
2. Monitor database performance
3. Regular backups of your database
4. Monitor application logs for errors
5. Set up health checks

## Troubleshooting

If you encounter issues:

1. Check application logs: `docker-compose logs web`
2. Verify environment variables are set correctly
3. Confirm database connectivity
4. Check static files are served correctly
5. Verify domain name settings

## Scaling Recommendations

1. Use a managed database service (AWS RDS, Google Cloud SQL, etc.)
2. Use CDN for static files (CloudFront, CloudFlare, etc.)
3. Use external Redis service for production
4. Implement monitoring and alerting
5. Set up automated backups