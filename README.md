# Fake News Score Service

## Requirements

Start both uclnlp (https://github.com/dagims/fakenewschallenge/tree/snet-service) and fnc (https://gitlab.com/nunet/odyssey-hackathon-2020-dev/-/tree/eskender_cpu) services (use the Dockerfile here)

Generate proto files

	./install.sh


## Install

Start grpc service

		python3.5 fake_news_score.py

Test grpc client

		python3.5 fns_grpc_client_test.py

