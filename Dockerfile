FROM continuumio/anaconda3:latest

WORKDIR /home

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY . .



