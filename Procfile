release: python manage.py makemigrations && python manage.py migrate
web: uvicorn ping_me_api.asgi:application --host=0.0.0.0 --port=${PORT:-8000} --workers=4 --log-level=info