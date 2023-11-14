#Deriving the latest base image
FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "client.py"]