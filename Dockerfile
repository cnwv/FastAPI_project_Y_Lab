FROM python:3.10-slim

RUN apt-get update && apt-get install -y python3 python3-pip

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod a+x docker/*.sh


