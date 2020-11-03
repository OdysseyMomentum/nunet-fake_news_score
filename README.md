
# Fake News Score Service

## Requirements

Start both [UCL Machine Reading](https://github.com/dagims/fakenewschallenge/tree/snet-service) and [Team SOLAT](https://gitlab.com/nunet/odyssey-hackathon-2020-dev/-/tree/eskender_cpu) fake news stance detection services (or use the Dockerfile here (instruction below))

Generate proto files

	./install.sh


## Install

Start grpc service

		python3.5 fake_news_score.py

Test grpc client

		python3.5 fns_grpc_client_test.py

## Docker

		sudo docker build -t IMAGE_NAME .

Run the three services inside docker
		
### Service on UCL Machine Reading stance detection
		python3.5 /root/uclnlp/pred.py # pick serve mode of grpc
		python3.5 /root/uclnlp/grpc_test_client.py
		
### Service on TEAM SOLAT stance detection
Download the [word2vec model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/) trained on Google News corpus. The file  `GoogleNews-vectors-negative300.bin`**
			
		python2 /root/fnc/tree_model/fnc.py # pick serve mode of grpc
		python2 /root/fnc/tree_model/grpc_test_client.py

### Fake news score service

		python3.5 /root/odyssey-hackathon-2020-dev/fake_news_score.py
		python3.5 /root/odyssey-hackathon-2020-dev/fns_grpc_client_test.py