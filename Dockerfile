FROM python:3.10
WORKDIR /code
USER root
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/