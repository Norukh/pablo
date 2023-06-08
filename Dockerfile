# Use Ubuntu as the base image
FROM arm64v8/ubuntu:22.04 as builder

# Set the working directory in the container
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
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
    libopenmpi-dev \
    openmpi-bin \
    apache2 \
    libapache2-mod-wsgi-py3

# Install Python
RUN apt-get install -y --no-install-recommends python3 python3-pip python3-dev python3-venv python3-distutils python3-apt

# Install TensorFlow
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Django and other dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run Django migrations
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic

# Stage 2: Final image
FROM arm64v8/ubuntu:22.04

# Install Apache and mod_wsgi
RUN apt-get update && apt-get install -y --no-install-recommends \
    apache2 \
    libapache2-mod-wsgi-py3

# Install Python
RUN apt-get install -y --no-install-recommends python3 python3-pip python3-dev python3-venv python3-distutils python3-apt

# Set the APACHE_LOG_DIR, APACHE_PID_FILE, APACHE_RUN_GROUP, and APACHE_RUN_USER environment variables
ENV APACHE_LOG_DIR=/var/log/apache2 \
    APACHE_PID_FILE=/var/run/apache2/apache2.pid \
    APACHE_RUN_GROUP=www-data \
    APACHE_RUN_USER=www-data

# Set the APACHE_RUN_DIR environment variable
ENV APACHE_RUN_DIR=/var/run/apache2

# Enable mod_wsgi
RUN a2enmod wsgi

# Copy the installed dependencies from the builder stage
COPY --from=builder /venv/ /venv/
COPY --from=builder /app/ /app/

# Set the working directory in the container
WORKDIR /app

# Set the secret key environment variable
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

# Copy the Apache configuration
COPY apache.conf /etc/apache2/sites-available/000-default.conf

# Set Python encoding environment variable
ENV PYTHONIOENCODING="UTF-8"

# Set the user and group ownership for Apache directories
RUN chown -R www-data:www-data /var/log/apache2 /var/run/apache2 /var/lock/apache2

# Enable the Apache configuration
RUN a2ensite 000-default

# Expose the required port
EXPOSE 80

# Run Apache in the foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]