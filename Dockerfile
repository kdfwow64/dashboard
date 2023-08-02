FROM python:3.11-slim AS build

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

RUN mkdir -p /root/.aws
COPY credentials /root/.aws
RUN mkdir -p /app/static

WORKDIR /app
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials python /app/manage.py collectstatic --noinput

EXPOSE 5000

# Run the Django application using Gunicorn (or other WSGI server)
CMD ["gunicorn", "dashboard.wsgi:application", "--bind", "0.0.0.0:5000"]
