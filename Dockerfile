# Use a Python base image
FROM python:3.9 as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . .

# Run Django migrations
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

# Make Migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN chmod a+x startup.sh

# Run Django
EXPOSE 8080
CMD ["/bin/bash", "-c", "./startup.sh"]