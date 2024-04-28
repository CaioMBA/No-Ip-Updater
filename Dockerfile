FROM python:latest

RUN apt update && apt upgrade -y && apt clean

WORKDIR /App

COPY requirements.txt /App

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]