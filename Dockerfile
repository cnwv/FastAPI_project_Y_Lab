FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh


