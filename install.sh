python3.5 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service_spec/fnc_stance_detection.proto

python3.5 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service_spec/uclnlpfnc.proto

python3.5 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service_spec/fake_news_score.proto