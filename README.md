# FakeNews Score Snet service 

Snet Marketplace service for FakeNews stance detection scoring [Athene FNC-1 Submission](https://github.com/hanselowski/athene_system) and [UCLNLP FNC-1 Submission](https://mr.cs.ucl.ac.uk/)

## Setup


	docker build -t fns_snet .
	
	# map daemon and service ports
	docker run -p 7002:7002 -p 7009:7009 -it fns_snet bash

	# snet request to service (using snet or the test script)
	snet client call odyssey-org fakenews-service default_group fn_score_calc '{"headline":"news_headline","body":"news_body"}' 
	
	python3 test_fake_news_score.py
