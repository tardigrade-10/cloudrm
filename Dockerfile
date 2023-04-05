FROM continuumio/anaconda3:latest

WORKDIR /home

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN python app.py

COPY requirements.txt requirements.txt