FROM --platform=linux/arm64 python:3.9

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html

COPY . /usr/src/app

# For Django
EXPOSE 8000
CMD ["python", "-v", "manage.py", "runserver", "0.0.0.0:8000"]