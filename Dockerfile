FROM ubuntu:18.04

RUN apt update; apt upgrade -y

RUN apt install -y vim \
                   git \
		               wget \
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

RUN cd /root && \
    git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc && \
    cd grpc && \
    git submodule update --init && \
    mkdir -p cmake/build && \
    cd cmake/build && \
    cmake ../.. && \
    make -j$(nproc) && \
    make install && \
    ldconfig

RUN cd /tmp/grpc && \
    cd thrid_party/protobuf && \
    make install & \
    ldconfig

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt update

RUN apt install -y python3.5 libpython3.5-dev

COPY . fake_news_score/
WORKDIR fake_news_score/