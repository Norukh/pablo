# Use a Python base image
FROM python:3.9

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

# Stage 2: Final image
# Use a Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /app/ /app/
COPY --from=builder /images /app/pablo_app/static

# Set the secret key environment variable
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Django
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]