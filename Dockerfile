FROM python:3.9-alpine
WORKDIR /app
COPY requeriments.txt /app
RUN pip install -r requeriments.txt
