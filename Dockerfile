FROM python:3.11-slim AS build

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

WORKDIR /app
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run the Django application using Gunicorn (or other WSGI server)
CMD ["gunicorn", "dashboard.wsgi:application", "--bind", "0.0.0.0:8000"]
