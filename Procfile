release: python manage.py makemigrations && python manage.py migrate
web daphne ping_me_api.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings-core.settings -v2