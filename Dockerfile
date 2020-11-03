FROM ubuntu:18.04

RUN apt update; apt upgrade -y

RUN apt install -y vim \
                   git \
		   wget \
                   curl \
                   clang \
                   cmake \
                   libtool \
                   autoconf \
                   zlib1g-dev \
                   pkg-config \
                   libc++-dev \
                   python3-dev \
                   python3-pip \
                   libudev-dev \
                   libgtest-dev \
                   libgflags-dev \
                   build-essential \
                   libusb-1.0.0-dev \
                   software-properties-common \
		   gfortran \
		   liblapack-dev \
		   libopenblas-dev \
		   python3-scipy \
		   python-dev \
		   python-scipy \
		   python-minimal \
		   python-nose

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python2 get-pip.py

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

RUN git clone -b eskender_cpu https://gitlab.com/nunet/odyssey-hackathon-2020-dev.git /root/fnc

WORKDIR /root/fnc

RUN python2 -m pip install -r requirements.txt

RUN git clone https://github.com/FakeNewsChallenge/fnc-1.git
RUN cp fnc-1/* tree_model/
RUN cp fnc-1/* deep_learning_model/
RUN rm -r fnc-1

RUN python2 nltk_downloader.py

RUN cp tree_model/test_stances_unlabeled.csv tree_model/test_stances_unlabeled_processed.csv

RUN python3.5 -m pip install numpy==1.11.3 \
                            scikit-learn==0.18.1 \
                            scipy==0.18.1 \
                            tensorflow==0.12.1 \
                            snet-cli

WORKDIR tree_model/service_spec

RUN python3.5 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. fnc_stance_detection.proto

RUN git clone -b snet-service https://github.com/dagims/fakenewschallenge /root/uclnlp

WORKDIR /root/uclnlp

RUN python3.5 -m grpc_tools.protoc \
              -I. \
              --python_out=. \
              --grpc_python_out=. \
              ./service_spec/uclnlpfnc.proto

COPY . /root/odyssey-hackathon-2020-dev/
WORKDIR /root/odyssey-hackathon-2020-dev/
