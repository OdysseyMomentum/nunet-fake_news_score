FROM snet_publish_service
  
RUN apt-get update && \
        apt-get install -y \
        curl \
        vim \
        nano \
        git \
        wget

RUN apt-get install -y python3 python3-pip

ENV SINGNET_REPOS=/opt/singnet
ENV ORGANIZATION_ID="odyssey-org"
ENV ORGANIZATION_NAME="odyssey"
ENV SERVICE_ID="fakenews-service"
ENV SERVICE_NAME="FAKE NEWS Service"
ENV SERVICE_IP="195.201.197.25"
ENV SERVICE_PORT="7009"
ENV DAEMON_PORT="7002"
ENV DAEMON_HOST="0.0.0.0"
ENV USER_ID="Amante"
ENV UCL_GRPC_ADD="demo.nunet.io:7007"
ENV ATHENE_GRPC_ADD="demo.nunet.io:7008"

EXPOSE 7002:7002
EXPOSE 7009:7009

RUN wget https://github.com/fullstorydev/grpcurl/releases/download/v1.1.0/grpcurl_1.1.0_linux_x86_64.tar.gz
RUN tar -xvzf grpcurl_1.1.0_linux_x86_64.tar.gz
RUN chmod +x grpcurl
RUN mv grpcurl /usr/local/bin/grpcurl

COPY . /${SINGNET_REPOS}/fns
WORKDIR /${SINGNET_REPOS}/fns

RUN pip3 install -r requirements.txt

RUN sh buildproto.sh

CMD ["python3", "run_fake_news_score.py", "--daemon-config", "snetd.config.json"]
