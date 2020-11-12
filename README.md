
# Fake News Score Service

A service that wraps average score from [UCL Machine Reading](https://gitlab.com/nunet/fake-news-detection/uclnlp) and [Athene](https://gitlab.com/nunet/fake-news-detection/athene) fake news stance detection services 

## Requirements

Point to running ATHENE_GRPC_PORT and UCL_GRPC_PORT instances in the environmental variables

## Install

		sudo docker build -t IMAGE_NAME .

Start grpc service

		python3 fake_news_score.py

Test grpc client

		python3 fns_grpc_client_test.py
