FROM python:3.8.13-slim-buster
# позволяет выводить print в консоль
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install netcat -y
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000
