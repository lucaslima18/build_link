# First Stage
FROM python:3.12.6 as base

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY . .

RUN apt update

RUN apt-get install -y build-essential \ 
    python3-dev python3-pip unixodbc-dev \ 
    libmysql++-dev curl git libaio1 unzip \
    tdsodbc \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
