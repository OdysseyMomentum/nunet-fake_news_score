python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/service_spec/athenefnc.proto

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/service_spec/uclnlp_service.proto

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service/service_spec/fake_news_score.proto
