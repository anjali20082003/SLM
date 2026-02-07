Write-Host "SLM Application Deployment Script" -ForegroundColor Green

# Check if .env file exists
if (!(Test-Path ".env")) {
    Write-Host "Creating .env file from example..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Copied .env.example to .env" -ForegroundColor Green
        Write-Host "Please update the .env file with your production settings before continuing." -ForegroundColor Yellow
    } else {
        Write-Host "No .env.example file found. Please create a .env file with your production settings." -ForegroundColor Red
        exit 1
    }
}

# Build and start the production services
Write-Host "Starting production deployment..." -ForegroundColor Green
docker-compose -f docker-compose.prod.yml up -d --build

Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Green
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

Write-Host "Collecting static files..." -ForegroundColor Green
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Your application should now be available at http://localhost" -ForegroundColor Green
Write-Host ""
Write-Host "To create a superuser account, run:" -ForegroundColor Yellow
Write-Host "docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser" -ForegroundColor White