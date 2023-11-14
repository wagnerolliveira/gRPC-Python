#Deriving the latest base image
FROM python:latest

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 50051

CMD ["python3", "server.py"]