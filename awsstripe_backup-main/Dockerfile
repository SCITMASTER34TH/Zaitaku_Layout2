# pull official base image
FROM python:3.8

# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV DEBUG 0

# set work directory
WORKDIR /app

RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run gunicorn
CMD python manage.py runserver 0.0.0.0:80
#CMD python manage.py runserver 0.0.0.0:8000