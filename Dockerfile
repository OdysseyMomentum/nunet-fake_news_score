FROM ubuntu:18.04

RUN sed -i -e 's/http:\/\/archive.ubuntu.com/http:\/\/be.archive.ubuntu.com/' /etc/apt/sources.list

RUN apt update; apt upgrade -y

RUN apt install -y vim \
                   curl \
                   git \
                   wget \
                   curl \ 
                   cmake \
                   libtool \
                   pkg-config \
                   libc++-dev \
                   python3-dev \
                   python3-pip \
                   libgflags-dev \
                   libudev-dev \
                   libgtest-dev \
                   build-essential \
                   libusb-1.0.0-dev \
                   software-properties-common

COPY . fake_news_score/
WORKDIR fake_news_score/

RUN python3 -m pip install -r requirements.txt
# build proto
RUN ./install.sh
