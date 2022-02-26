FROM python:3.6-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    python3-dev \
    build-essential
    # sqlite

ENV FLASK_APP api.py

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --src /usr/local/src

COPY src .

# WORKDIR src

EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0"]