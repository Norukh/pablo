# Use the official Python image as the base image
FROM python:3.9-slim-buster as builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libblas-dev \
    liblapack-dev \
    libhdf5-dev \
    libhdf5-serial-dev \
    libatlas-base-dev \
    gfortran \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libopenblas-dev \
    libopenblas-base \
    libopenmpi-dev \
    openmpi-bin \
    && pip install --no-cache-dir numpy==1.21.0

# Install TensorFlow
RUN pip install --no-cache-dir tensorflow

# Install Django and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run Django migrations
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic

# Stage 2: Final image
FROM python:3.9-slim-buster

# Install Apache and mod_wsgi
RUN apt-get update && apt-get install -y --no-install-recommends \
    apache2 \
    libapache2-mod-wsgi-py3

# Enable mod_wsgi
RUN a2enmod wsgi

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /app/ /app/

# Set the working directory in the container
WORKDIR /app

# Set the secret key environment variable
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

# Copy the Apache configuration
COPY apache.conf /etc/apache2/sites-available/000-default.conf

# Expose the required port
EXPOSE 8000

# Run Apache in the foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]