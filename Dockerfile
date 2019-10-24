FROM python:3.7-alpine

WORKDIR /opt/push-deploy

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
