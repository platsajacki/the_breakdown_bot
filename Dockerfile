FROM python:3.12

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
