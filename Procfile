release: python manage.py makemigrations && python manage.py migrate
web: gunicorn ping_me_api.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

