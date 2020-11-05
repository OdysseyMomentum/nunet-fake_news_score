
# Fake News Score Service

A service that wraps average score from [UCL Machine Reading](https://github.com/dagims/fakenewschallenge/tree/snet-service) and [Team SOLAT](https://gitlab.com/nunet/odyssey-hackathon-2020-dev/-/tree/eskender_cpu) fake news stance detection services 

## Requirements

Point to running FNC_GRPC_PORT and UCL_GRPC_PORT instances in fake_news_score.py

## Install

		sudo docker build -t IMAGE_NAME .

Start grpc service

		python3.5 fake_news_score.py

Test grpc client

		python3.5 fns_grpc_client_test.py
