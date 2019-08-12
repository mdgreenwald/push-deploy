FROM python:3-slim-stretch

WORKDIR /opt/push-deploy

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

