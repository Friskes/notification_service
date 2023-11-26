FROM python:3.8.13-slim-buster
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000
